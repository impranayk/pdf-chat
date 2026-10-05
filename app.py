import re
import zlib

import chromadb
import ollama
import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

st.title("Chat with your PDF")
pdf = st.file_uploader("Drop a PDF here", type="pdf") or open("HR_Policy.pdf", "rb")


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def build_store(name, _data):
    pages = [p.extract_text() for p in PdfReader(_data).pages]
    store = chromadb.EphemeralClient().get_or_create_collection(name)
    nums = range(1, len(pages) + 1)
    store.upsert(ids=[f"page-{n}" for n in nums], documents=pages,
                 embeddings=load_model().encode(pages).tolist(), metadatas=[{"page": n} for n in nums])
    return store


def ask(prompt):
    """Online (a GROQ_API_KEY secret is set): free cloud API. On your laptop: local Ollama."""
    try:
        key = st.secrets["GROQ_API_KEY"]
    except Exception:
        key = None
    messages = [{"role": "user", "content": prompt}]
    if key:
        from groq import Groq
        return Groq(api_key=key).chat.completions.create(model="openai/gpt-oss-20b", messages=messages).choices[0].message.content
    return ollama.chat(model="llama3.2", messages=messages)["message"]["content"]


store = build_store(f"doc-{zlib.crc32(pdf.name.encode())}", pdf)
st.caption(f"Reading: {pdf.name} · {store.count()} pages")

if question := st.chat_input("Ask about your PDF"):
    st.chat_message("user").write(question)
    hits = store.query(query_embeddings=load_model().encode([question]).tolist(), n_results=3)
    pages = [m["page"] for m in hits["metadatas"][0]]
    context = "\n\n".join(f"[page {n}] {d}" for n, d in zip(pages, hits["documents"][0]))
    prompt = f"""Context:
{context}

Question: {question}

Answer using ONLY the context above. If the answer is not there, say "I don't know."
Finish with one last line exactly like: SOURCE: page 4"""
    answer = ask(prompt)
    found = re.search(r"SOURCE:\s*page\s*(\d+)", answer, re.I)
    answer = re.sub(r"\s*SOURCE:.*$", "", answer, flags=re.I | re.S).strip()
    if found and int(found.group(1)) in pages:
        source = int(found.group(1))
    else:  # model forgot the line: pick the page sharing the most words with the answer
        words = set(re.findall(r"\w+", answer.lower()))
        source = max(zip(pages, hits["documents"][0]), key=lambda p: len(words & set(re.findall(r"\w+", p[1].lower()))))[0]
    with st.chat_message("assistant"):
        st.write(answer)
        if "don't know" not in answer.lower():
            st.caption(f"Source: page {source}")

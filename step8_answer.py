import chromadb
import ollama
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
store = chromadb.PersistentClient(path="hr_db").get_collection("hr_policy")

question = "How many vacation days do I get?"
hits = store.query(query_embeddings=model.encode([question]).tolist(), n_results=3)

context = "\n\n".join(
    f"[page {m['page']}] {d}" for m, d in zip(hits["metadatas"][0], hits["documents"][0])
)
prompt = f"""Answer using ONLY the context below, and say which page you used.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}"""

reply = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
print(reply["message"]["content"])

import ollama

reply = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Explain RAG in one sentence."}],
)

print(reply["message"]["content"])

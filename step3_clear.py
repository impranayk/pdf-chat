import ollama

reply = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "What is retrieval-augmented generation? One sentence."}],
)

print(reply["message"]["content"])

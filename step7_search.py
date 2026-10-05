import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
store = chromadb.PersistentClient(path="hr_db").get_collection("hr_policy")

question = "How many vacation days do I get?"
q = model.encode([question]).tolist()

hits = store.query(query_embeddings=q, n_results=3)
for meta, dist in zip(hits["metadatas"][0], hits["distances"][0]):
    print("page", meta["page"], " distance", round(dist, 2))

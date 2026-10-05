import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

reader = PdfReader("HR_Policy.pdf")
pages = [" ".join(p.extract_text().splitlines()[2:]) for p in reader.pages]

model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(pages).tolist()
nums = range(1, len(pages) + 1)

db = chromadb.PersistentClient(path="hr_db")
store = db.get_or_create_collection("hr_policy")
store.upsert(
    ids=[f"page-{n}" for n in nums],
    documents=pages,
    embeddings=vectors,
    metadatas=[{"page": n} for n in nums],
)
print(store.count(), "pieces saved in hr_db/")

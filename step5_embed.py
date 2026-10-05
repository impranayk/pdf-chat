from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

reader = PdfReader("HR_Policy.pdf")
chunks = []
for num, page in enumerate(reader.pages, start=1):
    lines = page.extract_text().splitlines()[2:]  # skip the 2 footer lines
    chunks.append({"page": num, "text": " ".join(lines)})

model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode([c["text"] for c in chunks])

print(len(chunks), "chunks")
print(len(vectors[3]), "numbers for page 4")
print(vectors[3][:5].round(3))

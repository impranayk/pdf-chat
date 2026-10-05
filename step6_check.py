import chromadb

store = chromadb.PersistentClient(path="hr_db").get_collection("hr_policy")
print(store.count(), "pieces still here")

page4 = store.get(ids=["page-4"])
print(page4["metadatas"][0], page4["documents"][0][:45])

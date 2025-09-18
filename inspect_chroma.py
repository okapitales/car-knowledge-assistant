from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = "./chroma_db"

# Load embeddings model (must match the one you used before)
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Reload your Chroma DB
vectorstore = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embedding_model
)

# Sneak peek
print("📂 Collections available:", vectorstore._collection.name)

# How many vectors are stored
count = vectorstore._collection.count()
print(f"🔢 Total stored vectors: {count}")

# Show first 3 documents
docs = vectorstore.similarity_search("car", k=3)
for i, doc in enumerate(docs, start=1):
    print(f"\n--- Result {i} ---")
    print(doc.page_content[:300], "...")

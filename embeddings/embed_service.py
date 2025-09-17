from fastapi import FastAPI, Query
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import pandas as pd
from pathlib import Path

# Directories
DATA_FILE = Path("./processed/car_data.csv")   # chunks from Day 1
DB_DIR = "./chroma_db"

# Init FastAPI
app = FastAPI(title="Car Knowledge Assistant - Embeddings Service")

# Embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Global vectorstore
vectorstore = None

# Data model
class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


@app.on_event("startup")
def load_embeddings():
    global vectorstore
    if Path(DB_DIR).exists():
        # Load existing DB
        vectorstore = Chroma(persist_directory=DB_DIR,
                             embedding_function=embedding_model)
    else:
        # Build from chunks
        if not DATA_FILE.exists():
            raise RuntimeError("No processed chunks found. Run ingestion first!")
        df = pd.read_csv(DATA_FILE)
        texts = df["text"].tolist()
        vectorstore = Chroma.from_texts(
            texts, embedding_model, persist_directory=DB_DIR
        )
        vectorstore.persist()
    print("✅ Embedding service ready")


@app.post("/embed")
def embed():
    """Rebuild embeddings from car_data.csv"""
    global vectorstore
    if not DATA_FILE.exists():
        return {"error": "No processed data found"}
    df = pd.read_csv(DATA_FILE)
    texts = df["text"].tolist()
    vectorstore = Chroma.from_texts(
        texts, embedding_model, persist_directory=DB_DIR
    )
    vectorstore.persist()
    return {"status": "Embeddings stored", "count": len(texts)}


@app.post("/search")
def search(request: SearchRequest):
    """Semantic search for a query"""
    global vectorstore
    if not vectorstore:
        return {"error": "Vectorstore not initialized"}
    docs = vectorstore.similarity_search(request.query, k=request.top_k)
    results = [doc.page_content for doc in docs]
    return {"query": request.query, "results": results}

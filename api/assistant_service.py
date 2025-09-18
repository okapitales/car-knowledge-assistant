from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import os
from api.slm_gateway import slm_gateway


from dotenv import load_dotenv
load_dotenv()  # load variables from .env file

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_anthropic import ChatAnthropic

# ---- Config ----
DB_DIR = "./chroma_db"
DATA_FILE = Path("./processed/car_data.csv")

EMBED_MODEL = "all-MiniLM-L6-v2"
LOCAL_LLM = "google/flan-t5-base"
USE_CLAUDE = True   # 👈 switch between Claude and local

# ---- FastAPI init ----
app = FastAPI(title="Car Knowledge Assistant")

# ---- Request Models ----
class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

class AskRequest(BaseModel):
    question: str
    top_k: int = 3

# ---- Global state ----
embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
vectorstore = None
qa_chain = None

# ---- Root endpoint ----
@app.get("/")
def root():
    return {
        "message": "🚗 Car Knowledge Assistant API is running!",
        "endpoints": ["/embed", "/search", "/ask", "/docs"],
        "llm_mode": "Claude" if USE_CLAUDE else "Local Flan-T5"
    }

# ---- Startup: load DB + LLM ----
@app.on_event("startup")
def load_vectorstore():
    global vectorstore, qa_chain

    if not Path(DB_DIR).exists():
        print("⚠️ No Chroma DB found. Run /embed first.")
        return

    vectorstore = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding_model
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # ---- Choose LLM ----
    if USE_CLAUDE:
        print("🤖 Using Anthropic Claude LLM")
        llm = ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
            temperature=0,
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    else:
        print("🤖 Using Local HuggingFace LLM (Flan-T5)")
        tokenizer = AutoTokenizer.from_pretrained(LOCAL_LLM)
        model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_LLM)  # ✅ correct class
        gen_pipeline = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512
        )
        llm = HuggingFacePipeline(pipeline=gen_pipeline)

    # ---- Prompt ----
    template = """
    You are a helpful Volkswagen car assistant.
    Use the following context to answer the user question.
    If the answer is not in the context, say you don't know.

    Context: {context}
    Question: {question}
    Answer:
    """
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

    # ---- Build RAG chain ----
    global qa_chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )
    print("✅ Loaded Chroma DB and RAG pipeline")

# ---- /embed ----
@app.post("/embed")
def embed():
    global vectorstore, qa_chain

    if not DATA_FILE.exists():
        return {"error": "No processed data found"}

    df = pd.read_csv(DATA_FILE)
    texts = df["text"].dropna().astype(str).tolist()

    vectorstore = Chroma.from_texts(
        texts, embedding_model, persist_directory=DB_DIR
    )
    vectorstore.persist()

    return {"status": "Embeddings stored", "count": len(texts)}

# ---- /search ----
@app.post("/search")
def search(request: SearchRequest):
    global vectorstore
    if not vectorstore:
        return {"error": "Vectorstore not initialized. Run /embed first."}
    docs = vectorstore.similarity_search(request.query, k=request.top_k)
    results = [doc.page_content for doc in docs]
    return {"query": request.query, "results": results}

# ---- /ask ----
#@app.post("/ask")
#def ask(request: AskRequest):
#    global qa_chain
 #   if not qa_chain:
 #       return {"error": "RAG pipeline not initialized. Run /embed first."}
 #   answer = qa_chain.run(request.question)
 #   return {"question": request.question, "answer": answer}
# ---- /ask ----
@app.post("/ask")
def ask(request: AskRequest):
    global qa_chain
    if not qa_chain:
        return {"error": "RAG pipeline not initialized. Run /embed first."}

    # Pass through SLM gateway
    slm_result = slm_gateway(request.question)

    if slm_result["action"] == "block":
        return {
            "question": request.question,
            "status": "blocked",
            "reason": slm_result["reason"]
        }

    cleaned_q = slm_result["cleaned"]

    # Run through RAG chain
    answer = qa_chain.run(cleaned_q)

    return {
        "original_question": request.question,
        "processed_question": cleaned_q,
        "answer": answer,
        "slm_reason": slm_result["reason"]
    }

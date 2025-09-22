# Car Knowledge Assistant (CKA) or Automotive Sales Knowledge (ASK)

**An AI-powered Retrieval-Augmented Assistant that helps VW Sales Advisors and customers quickly understand vehicle features, diagnose issues, and streamline dealer handoffs.**

---

## What is this project about?

The Car Knowledge Assistant (CKA) is a **GenAI-driven knowledge tool** designed to support the automotive sales and service process.  
It uses Retrieval-Augmented Generation (RAG) to pull answers from owner manuals, feature guides, FAQs, and dealer documentation.  

The system can:
- Provide **VIN-aware answers** tailored to a specific model/trim.
- Ask clarification questions to refine user queries.
- Summarize issues and generate a **Dealer Handoff Package** (chat summary + suspected issue + availability).
- Keep responses grounded in official VW sources.

The result: **fewer escalations, faster conversations, and happier customers.**

---

## Why is it beneficial for VW Sales and the company?

**For Sales Advisors**
- Instant answers about trim differences, features, or setup steps.
- Less time spent searching manuals, more time selling.
- Clearer communication with customers, boosting confidence in the brand.

**For VW (Business Impact)**
- Improves **sales experience and conversion rates**.
- Reduces **support overhead** with accurate self-service.
- Enhances **customer satisfaction (NPS)** by resolving confusion quickly.
- Provides **analytics** on top customer questions, helping VW refine documentation and marketing.

---

## Tech Stack

### ✅ Current Tech Stack (Implemented)

- **API Framework**
  - FastAPI (REST API endpoints)
  - Pydantic (request/response validation)
  - python-dotenv (environment variable management)

- **LLMs & Embeddings**
  - Anthropic Claude (primary LLM via LangChain integration)
  - HuggingFace Transformers (Flan-T5, DistilBERT for zero-shot classification)
  - Sentence-Transformers (e.g., `all-MiniLM-L6-v2` for embeddings)

- **Vector Database**
  - Chroma (local persistence for embeddings and retrieval)

- **NLP Preprocessing**
  - spaCy (`en_core_web_sm`) for lemmatization and stopword removal
  - Regex-based cleaning for normalization

- **LangChain Components**
  - RetrievalQA pipeline
  - PromptTemplate-based query formatting

- **Utilities & Testing**
  - pandas (CSV ingestion and processing)
  - pytest (unit testing of ingestion and text-cleaning functions)

---

### 🚀 Future Enhancements (Planned)

- **Containerization & Orchestration**
  - Docker & docker-compose for local multi-service setups
  - Kubernetes manifests for scalable deployment

- **Observability & Evaluation**
  - Langfuse or Langtrace for tracing and monitoring
  - RAGAS for automated evaluation of retrieval quality

- **Event & Streaming**
  - Kafka integration for async telemetry and data pipelines

- **CI/CD**
  - GitHub Actions for automated builds, tests, and deployment

- **Integrations**
  - Salesforce (SOQL queries for CRM data)
  - Dealer scheduling & CRM API connections

- **Multi-Modal Features**
  - Image-based input (e.g., dashboard/warning light recognition)
  - Voice-based queries

- **Edge/Offline Deployment**
  - Kiosk/iPad-friendly deployments
  - Offline embedding packs for low-connectivity environments

---

## Current Status

- Runs locally using Python/FastAPI.  
- Vector database stored locally (no container orchestration yet).  
- Focused on RAG, LLM orchestration, and sales-support use cases.  
- **Docker/Kubernetes not implemented yet** due to GitHub Codespaces storage limits.  

---

## License

This project is open-source and available under the **MIT License**.  
See the [LICENSE](./LICENSE) file for details.

---

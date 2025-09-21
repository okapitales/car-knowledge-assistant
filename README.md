# Car Knowledge Assistant (CKA)

**An AI-powered Retrieval-Augmented Assistant that helps VW Sales Advisors and customers quickly understand vehicle features, diagnose issues, and streamline dealer handoffs.**

---

## What is this project about?

The Car Knowledge Assistant (CKA) is a **GenAI-driven knowledge tool** for the automotive sales and service process.  
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

## Tech Stack Used

- **Python** (FastAPI for APIs, orchestration with LangGraph/LangChain)  
- **Vector Database**: Chroma (local dev); supports FAISS, Pinecone, or Weaviate in production  
- **LLM**: Anthropic Claude (configurable, pluggable)  
- **Embeddings**: Sentence Transformers / Open-source models  
- **Data Science Libraries**: NumPy, pandas, scikit-learn  
- **Evaluation & Observability**: RAGAS, Langfuse/Langtrace  
- **Version Control & CI/CD**: GitHub Actions  

---

## Current Status

- Runs locally using Python/FastAPI.  
- Vector database stored locally (no container orchestration yet).  
- Focused on RAG, LLM orchestration, and sales-support use cases.  
- **Docker/Kubernetes not implemented yet** due to GitHub Codespaces storage limits.  

---

## Future Enhancements

- **Containerization & Orchestration**
  - Add **Docker** for portable local environments.  
  - Add **docker-compose** for multi-service setup (API, retriever, vector DB, observability).  
  - Deploy on **Kubernetes** with manifests for API gateway, retriever, vector DB, and autoscaling.  

- **Advanced Features**
  - Stronger **VIN-awareness** (software versions, region-specific features).  
  - **Multi-modal support** (images of dashboard/warning lights).  
  - Inline **citations** linking back to official VW manuals.  
  - Dealer system integration: service calendars, CRM, and part availability.  
  - Automated content refresh pipelines for manuals/FAQs.  
  - A/B pipelines for experimenting with different prompting or retrieval methods.  
  - Offline/edge support for showroom iPads and kiosks.  

---

## License

MIT License

Copyright (c) 2025 Mujib Yunus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in  
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING  
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS  
IN THE SOFTWARE.

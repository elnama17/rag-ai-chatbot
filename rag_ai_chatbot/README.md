# RAG-ai-chatbot

![Build Status](https://github.com/elnama17/rag_ai_chatbot/actions/workflows/ci-build.yaml/badge.svg)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![3.12](https://img.shields.io/badge/Python-3.12-green.svg)](https://shields.io/)

---

Vallie: Friendly RAG AI Chatbot

Vallie is a friendly AI assistant powered by Amazon Bedrock LLM and optionally enhanced with RAG (Retrieval-Augmented Generation). Vallie can answer questions, provide insights, and fetch specific company knowledge when RAG is enabled.

Features

Conversational AI with a friendly personality.

Real-time streaming responses from the backend.

Optional RAG functionality to retrieve information from a knowledge base.

Dockerized frontend (Streamlit) and backend (FastAPI) services.

Interactive UI with chat history and clear chat option.

## Structure
```
------------
rag_ai_chatbot/
│
├── .github/
│   └── workflows/
│       └── ci-build.yaml
│
├── backend/
│   ├── assets/
│   │   ├── backend_endpoint.png
│   │   └── backend_logs.png
│   ├── app.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── .python-version
|   └── uv.lock
│
├── frontend/
│   ├── assets/
│   │   ├── llm_answer.png
│   │   └── rag_version.png
│   ├── app.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
|   ├── uv.lock
│   └── .python-version
├─ .gitignore
├─ docker-compose.yml
└─ README.md

--------
```

---

## 🛠️ Installation & Setup

### Run with Docker
```bash
# Build and start the containers
docker compose up --build

# Stop containers
docker compose down
```
## 📑 Notes

Ensure Docker Desktop is installed if using Docker.

If running backend independently, remember to create a .venv or use uv.

Frontend requires Node.js & npm/yarn if run outside Docker.

# RAG-based AI Chatbot

![Build Status](https://github.com/elnama17/rag_ai_chatbot/actions/workflows/ci-build.yaml/badge.svg)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![3.12](https://img.shields.io/badge/Python-3.12-green.svg)](https://shields.io/)

---

## 🤖 Vallie: Friendly RAG-based AI Chatbot

Vallie is a friendly AI assistant powered by Amazon Bedrock LLM and optionally enhanced with RAG (Retrieval-Augmented Generation). Vallie can answer questions, provide insights, and fetch specific company knowledge when RAG is enabled.

### ✨ Features
- Conversational AI with a friendly personality (**Vallie**).  
- Real-time **streaming responses** from the backend.  
- Optional **RAG functionality** to retrieve information from a knowledge base.  
- Dockerized **frontend (Streamlit)** and **backend (FastAPI)** services.  
- Interactive UI with **chat history** and **clear chat** option.  

## project structure
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

## ⚙️ Requirements

Before running the project, make sure you have the following installed:

- Python 3.9+

- uv (for dependency management and running the app)

- Docker

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/elnama17/rag-ai-chatbot.git
cd rag-ai-chatbot\rag_ai_chatbot
```
### 2. Create a .env file in the project root directory with your AWS Bedrock credentials:
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
KNOWLEDGE_BASE_ID=your_knowledge_base_id
```
### 3. Run with docker-compose up --build

### 4. Access the chatbot: 4. Access the Chatbot
```bash
Backend API: http://localhost:8000

If frontend is implemented: http://localhost:8501
```
## Docker Notes

Each service runs in its own container.

Logs can be checked with:
```bash
docker-compose logs backend
```
To stop:
```
docker-compose down
```

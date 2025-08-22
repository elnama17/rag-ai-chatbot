# RAG-based AI Chatbot

[![CI/CD Pipeline](https://github.com/elnama17/rag-ai-chatbot/actions/workflows/ci-cd.yaml/badge.svg)](https://github.com/elnama17/rag-ai-chatbot/actions/workflows/ci-cd.yaml)

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

### Query without RAG:
![ALt text](/frontend/assets/vallie_query.png)

### Query with RAG:

![ALt text](/frontend/assets/rag.png)


## project structure
```
------------
rag-ai-chatbot/
│
├── .github/
│   └── workflows/
│       └── ci-build.yaml
│
├── backend/
│   ├── assets/
│   │   ├── endpoints.png
|   |   ├── logs.png
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
│   │   ├── rag.png
|   |   ├── vallie_introduction.png
│   │   └── vallie_query.png
│   ├── app.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
|   ├── uv.lock
│   └── .python-version
├─ .gitignore
├─ LICENSE
├─ README.md
└─ docker-compose.yml

--------
```

---

## ⚙️ Requirements

Before running the project, make sure you have the following installed:

- Python 3.9+

- uv (for dependency management and running the app)

- Docker

## 🚀 Running the Project

### ✅ Run Locally

1. Clone the repository:

```
git clone https://github.com/elnama17/rag-ai-chatbot.git
cd <rag-ai-chatbot>
```


2. Create and configure .env file
Fill in the required environment variables (e.g., API keys, database credentials):
```AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
KNOWLEDGE_BASE_ID=your_knowledge_base_id
```

3. Start with Docker Compose:
```
docker-compose up --build
```

4. Open your browser and go to:
```
http://localhost:3000   # frontend
http://localhost:8000   # backend API
```
### 🌍 Run on AWS EC2

1. Launch an EC2 instance.

2. Choose Ubuntu 22.04 or Amazon Linux.

3. Open security groups for ports 22 (SSH), 80 (HTTP), and any others your app needs.

4. Install Docker & Docker Compose:
```
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
```

5. Clone your repository:
```
git clone https://github.com/elnama17/rag-ai-chatbot.git
cd <rag-ai-chatbot>
```

6. Run with Docker Compose:
```
docker-compose up --build -d
```


7. Access your app
In your browser, go to:
```bash
http://<EC2-PUBLIC-IP>
```
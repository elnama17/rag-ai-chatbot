import os
import json
import time
from dotenv import load_dotenv
import boto3
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, PlainTextResponse

# ----------------------
# Load environment
# ----------------------
load_dotenv()  # expects .env in project root

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
MODEL_ID = os.getenv("MODEL_ID")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")  # <-- add this in .env

# ----------------------
# AWS Bedrock clients
# ----------------------
client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

kb_client = boto3.client(
    "bedrock-agent-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

# ----------------------
# Vallie personality
# ----------------------
VALLIE_SYSTEM_PROMPT = """
You are Vallie, a friendly and conversational AI assistant.
Be helpful, polite, and engaging in your responses.
"""

# ----------------------
# Helper functions
# ----------------------
def create_body_json(prompt: str, system: str = ""):
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 10240,
        "system": system,
        "messages": [{"role": "user", "content": prompt}]
    })

def generate_llm_answer(prompt: str):
    """Normal LLM call: returns full text"""
    body_json = create_body_json(prompt)
    response = client.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body_json
    )
    message = json.loads(response['body'].read().decode('utf-8'))
    return message['content'][0]['text']

def generate_vallie_answer(prompt: str):
    """Vallie - Friendly AI assistant"""
    body_json = create_body_json(prompt, system=VALLIE_SYSTEM_PROMPT)
    response = client.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body_json
    )
    message = json.loads(response['body'].read().decode('utf-8'))
    return message['content'][0]['text']

def stream_llm_answer(prompt: str):
    """Streaming generator: yields chunks"""
    full_text = generate_llm_answer(prompt)
    chunk_size = 30
    for i in range(0, len(full_text), chunk_size):
        yield full_text[i:i+chunk_size]
        time.sleep(0.1)

def stream_vallie_answer(prompt: str):
    """Streaming generator: yields chunks"""
    full_text = generate_vallie_answer(prompt)
    chunk_size = 30
    for i in range(0, len(full_text), chunk_size):
        yield full_text[i:i+chunk_size]
        time.sleep(0.1)

# ----------------------
# Knowledge Base helpers
# ----------------------
def retrieve_from_kb(query: str, top_k: int = 3):
    """Query the knowledge base and return top results"""
    req = {
        "knowledgeBaseId": KNOWLEDGE_BASE_ID,
        "retrievalQuery": {"text": query},
        "retrievalConfiguration": {
            "vectorSearchConfiguration": {
                "numberOfResults": top_k
            }
        }
    }
    response = kb_client.retrieve(**req)
    candidates = response.get("retrievalResults", [])
    docs = [
        f"Document {i+1}: {doc['content']['text']}"
        for i, doc in enumerate(candidates)
        if "content" in doc and "text" in doc["content"]
    ]
    return "\n\n".join(docs)

def generate_rag_answer(user_query: str):
    """Combine KB retrieval with LLM generation"""
    kb_context = retrieve_from_kb(user_query)
    prompt = f"""
### Knowledge Base:
{kb_context}

### User Query:
{user_query}
"""
    return generate_llm_answer(prompt)

# ----------------------
# FastAPI app
# ----------------------
app = FastAPI(title="RAG AI Backend")

@app.get("/")
def root():
    return {"message": "Backend running! Use /api/chat-llm, /api/chat-llm-stream, /api/chat-rag, or /api/chat-llm-vallie"}

@app.get("/api/chat-llm")
def chat_llm(query: str = Query(...)):
    try:
        answer = generate_llm_answer(query)
        return PlainTextResponse(answer)
    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}")

@app.get("/api/chat-llm-stream")
def chat_llm_stream(query: str = Query(...)):
    try:
        return StreamingResponse(stream_llm_answer(query), media_type="text/plain")
    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}")

@app.get("/api/chat-rag")
def chat_rag(query: str = Query(...)):
    try:
        answer = generate_rag_answer(query)
        return PlainTextResponse(answer)
    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}")

@app.get("/api/chat-llm-vallie")
def chat_llm_vallie(query: str = Query(...)):
    """Vallie - Friendly AI assistant streaming"""
    try:
        return StreamingResponse(stream_vallie_answer(query), media_type="text/plain")
    except Exception as e:
        return PlainTextResponse(f"Error: {str(e)}")

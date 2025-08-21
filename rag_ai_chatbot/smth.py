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

# ----------------------
# AWS Bedrock client
# ----------------------
client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

# ----------------------
# Helper functions
# ----------------------
def create_body_json(prompt: str):
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 10240,
        "system": "",
        "messages": [{"role": "user", "content": prompt}]
    })

def generate_llm_answer(prompt: str):
    """
    Normal LLM call: returns full text
    """
    body_json = create_body_json(prompt)
    response = client.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body_json
    )
    message = json.loads(response['body'].read().decode('utf-8'))
    return message['content'][0]['text']

def stream_llm_answer(prompt: str):
    """
    Streaming generator: yields chunks
    """
    full_text = generate_llm_answer(prompt)  # Get full text from LLM
    chunk_size = 30  # characters per chunk
    for i in range(0, len(full_text), chunk_size):
        yield full_text[i:i+chunk_size]
        time.sleep(0.1)  # simulate streaming

# ----------------------
# FastAPI app
# ----------------------
app = FastAPI(title="RAG AI Backend")

@app.get("/")
def root():
    return {"message": "Backend running! Use /api/chat-llm or /api/chat-llm-stream"}

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

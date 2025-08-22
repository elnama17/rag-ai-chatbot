import os
import streamlit as st
import requests

# --- Page config ---
st.set_page_config(page_title="Vallie Chatbot 🤖", layout="wide")
st.markdown("<h1 style='text-align:center;'>🤖 Vallie Chatbot</h1>", unsafe_allow_html=True)

# --- Backend URL ---
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# --- Session state for chat history ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Sidebar for info / controls ---
with st.sidebar:
    st.markdown("### Chatbot Controls")
    if st.button("Clear chat"):
        st.session_state["messages"] = []
        st.experimental_rerun()
    st.markdown("---")
    st.markdown("""
### 🌟 Meet Vallie, your friendly AI assistant! 🤖

Hi there! I'm **Vallie**, and I'm here to help you find answers, share insights, and make learning fun and easy!\n
You can use the **RAG option** to fetch info about the policies of the Azercell Telecom LLC! 💡✨
""")
    # Add checkbox to toggle RAG
    use_rag = st.checkbox("RAG (Use Knowledge Base)", value=True)

# --- Display chat history ---
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(f"💬 {msg['content']}")
    else:
        st.chat_message("assistant").markdown(f"🤖 {msg['content']}")

# --- User input ---
if prompt := st.chat_input("Type your message..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(f"💬 {prompt}")

    # Choose endpoint based on checkbox
    endpoint = "/api/chat-rag" if use_rag else "/api/chat-llm-vallie"

    try:
        # Streaming response from backend
        response = requests.get(
            f"{BACKEND_URL}{endpoint}",
            params={"query": prompt},
            stream=True,
            timeout=60
        )
        response.raise_for_status()

        # Stream chunk by chunk
        message_placeholder = st.chat_message("assistant").empty()
        full_response = ""
        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                full_response += chunk
                message_placeholder.markdown(f"🤖 {full_response} ▌")  # typing cursor

        # Save assistant message
        st.session_state["messages"].append({"role": "assistant", "content": full_response})

    except requests.exceptions.RequestException as e:
        st.error(f"Error: Backend not reachable\n{e}")

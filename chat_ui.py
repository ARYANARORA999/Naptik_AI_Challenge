import os
import json
import streamlit as st
from rag_pipeline import ask_rag_query

# --- Setup ---
st.set_page_config(page_title="🧠 SleepBot RAG", layout="centered")

st.title("😴 SleepBot — Your Sleep & Health Chatbot")
st.markdown("Ask me anything about your sleep, steps, heart rate, caffeine, jet lag, and more! 🧬")

# --- Persistent Chat History ---
memory_path = "data/chat_history.json"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "rag_context" not in st.session_state:
    st.session_state.rag_context = []

# Load existing history from disk
if os.path.exists(memory_path) and not st.session_state.chat_history:
    with open(memory_path, "r") as f:
        st.session_state.chat_history = json.load(f)

# --- Show History ---
with st.expander("🗂 Chat History", expanded=False):
    for turn in st.session_state.chat_history:
        st.markdown(f"**🧑 You:** {turn['user']}")
        st.markdown(f"**🤖 RAG Bot:** {turn['RAG Assistant']}")

# --- Chat Box ---
query = st.chat_input("Type your question here...")
if query:
    with st.spinner("Thinking..."):
        response = ask_rag_query(query, history=st.session_state.rag_context)

        st.markdown(f"**🧑 You:** {query}**")
        st.markdown(f"**🤖 RAG Bot:** {response}**")

        # Save to memory
        st.session_state.chat_history.append({
            "user": query,
            "RAG Assistant": response
        })
        with open(memory_path, "w") as f:
            json.dump(st.session_state.chat_history, f, indent=2)

        # Update RAG sliding window
        st.session_state.rag_context.append(f"You: {query}")
        st.session_state.rag_context.append(f"RAG Bot: {response}")
        st.session_state.rag_context = st.session_state.rag_context[-4:]

# --- Reset Button ---
st.markdown("---")
if st.button("🔄 Reset Chat"):
    st.session_state.chat_history = []
    st.session_state.rag_context = []
    if os.path.exists(memory_path):
        os.remove(memory_path)
    st.rerun()

st.markdown("---")
st.caption("🧠 Powered by Gemini + FAISS + LangChain | Made with 💙 for Naptick AI Challenge")

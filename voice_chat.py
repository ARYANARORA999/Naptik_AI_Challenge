import os
import json
import whisper
from utils.recorder import record_audio
from utils.speaker import speak_text
from rag_pipeline import get_chat_response

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Paths
memory_path = "data/chat_history.json"
chat_data = []
rag_context_window = []

# Load history if exists
if os.path.exists(memory_path):
    with open(memory_path, "r") as f:
        chat_data = json.load(f)
    for m in chat_data[-4:]:
        rag_context_window.append(f"You: {m['user']}")
        rag_context_window.append(f"RAG Bot: {m['RAG Assistant']}")
    rag_context_window = rag_context_window[-4:]

def transcribe(file="input.wav"):
    model = whisper.load_model("base")
    result = model.transcribe(file)
    return result["text"]

def normalize_query(query: str) -> str:
    query = query.strip().lower()

    # Normalize common vague queries
    if "how was my sleep on the next day" in query:
        return "how was my sleep on the next day?"
    if "how was my sleep on the previous day" in query:
        return "how was my sleep on the previous day?"
    if "how did i sleep on that day" in query:
        return "how did I sleep on that day?"
    return query

def main():
    print("🎙️ Voice-enabled SleepBot — say 'exit' to quit")
    while True:
        record_audio()
        raw_query = transcribe()
        query = normalize_query(raw_query)
        print(f"🧑 You said: {raw_query}")
        if query.lower() in ["exit", "quit"]:
            break
        response = get_chat_response(query, history=rag_context_window)
        print(f"🤖 SleepBot: {response}")
        speak_text(response)

        # Update memory
        chat_data.append({
            "user": query,
            "RAG Assistant": response
        })
        with open(memory_path, "w") as f:
            json.dump(chat_data, f, indent=2)

        rag_context_window.append(f"You: {query}")
        rag_context_window.append(f"RAG Bot: {response}")
        rag_context_window[:] = rag_context_window[-4:]

if __name__ == "__main__":
    main()

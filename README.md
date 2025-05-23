# 💤 Naptik AI Challenge — SleepBot 💬🎙️

A conversational health assistant powered by **Gemini**, **LangChain**, and **local voice tools**, providing intelligent, voice-enabled insights over structured personal sleep, health, and location data.

---

## 🔍 Features

- 🤖 **Chatbot using Gemini** (via LangChain)
- 📁 **RAG pipeline** over JSON sleep datasets (diary, wearable, profile, location)
- 🧠 **FAISS-based vector search** with smart filtering
- 🔄 **Sliding window memory** for contextual follow-up questions
- 🌐 **Streamlit Web Interface** with persistent memory and history
- 🎙️ **Voice-to-Voice Assistant** with:
  - 🗣️ **Speech-to-text** using OpenAI Whisper (local)
  - 🗨️ **RAG Query** from shared logic
  - 🔊 **Text-to-speech** using Edge-TTS (local, high-quality)
- 🧠 **Temporal memory**: references like "that day", "next day", and "previous day" are understood even across data types.

---

## 🛠️ Installation

### ✅ Clone & Setup Environment

```bash
git clone https://github.com/ARYANARORA999/Naptik_AI_Challenge.git
cd Naptik_AI_Challenge

# (Optional) Create a virtual environment
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt
```

---

## 💻 Run Task1 ChatBot via CLI

```bash
python app.py
```

Use the terminal to interact with your AI assistant. It supports:
- "How was my sleep on April 21, 2025?"
- "What did my diary say on April 12?"
- "How was my sleep the Next Day?"
- "How many steps did I walk on that day?"

---

## 💻 Run Task2 Voice Assistant ChatBoot via CLI

```bash
python app.py
```

Use the terminal to interact with your AI assistant. It supports:
- "How was my sleep on April 21, 2025?"
- "What did my diary say on April 12?"
- "How was my sleep the Next Day?"
- "How many steps did I walk on that day?"

---

## 🌐 Run via Web GUI (Streamlit)

```bash
streamlit run chat_ui.py
```

- Interactive chatbot interface
- Context-aware conversation
- Memory persists across sessions
- Reset button and usage logging

---

## 📁 Data Files (inside `/data` folder)

| File Name          | Description                            |
|--------------------|----------------------------------------|
| `wearable_data.json` | Daily sleep, REM, deep sleep, HR, steps |
| `sleep_diary.json`   | Subjective notes about sleep per day    |
| `location_data.json` | Location and timezone per date          |
| `user_profile.json`  | Name, age, sleep goal, preferred hours  |
| `chat_history.json`  | Conversation log (auto-generated)       |

---
## 📁 Util Files (inside `/utils` folder)

| File Name        | Description                                        |
| ---------------- | -------------------------------------------------- |
| `recorder.py`    | Records audio input using `sounddevice`            |
| `speaker.py`     | Converts text to speech using Edge-TTS             |
| `responder.py`   | (If used separately) Handles LLM response logic    |
| `transcriber.py` | (Optional) Transcription logic wrapper for Whisper |


---

## ✨ Example Queries

- **"Where was I on April 24, 2025?"**
- **"Show my average sleep in April."**
- **"How many steps did I walk on that day?"**
- **"How many hours did I sleep on that day?"**

---

## 🧩 Tech Stack

- 🔗 LangChain
- 🌐 Gemini 1.5 / 2.0 (via `langchain_google_genai`)
- 🧠 FAISS for vector similarity
- 🧾 JSON structured data (RAG)
- 🖥️ Streamlit UI
- 🗨️ OpenAI Whisper (local STT)
- 🔉 Edge-TTS (local high-quality TTS)

---

## 👨‍💻 Author

Made with 💙 by Aryan Arora for the **Naptik AI Challenge**

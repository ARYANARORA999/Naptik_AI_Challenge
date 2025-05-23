import os
import json
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from rag_pipeline import ask_rag_query

#  Chat memory file
memory_path = "data/chat_history.json"
chat_data = []

#  Load past memory
if os.path.exists(memory_path) and os.path.getsize(memory_path) > 0:
    with open(memory_path, "r") as f:
        chat_data = json.load(f)

#  LangChain memory for tool-based agent
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
for m in chat_data:
    memory.chat_memory.add_user_message(m["user"])
    memory.chat_memory.add_ai_message(m["RAG Assistant"])

#  Gemini setup
os.environ["GOOGLE_API_KEY"] = "AIzaSyBeZmM4OosHckKTTPeQW08ymisgD0uJKrs"
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.4)

#  LangChain agent with tools
agent = initialize_agent(
    tools=[],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

#  Main Chat Loop
def main():
    print("🧠 SleepBot (Gemini + RAG) — type 'exit' to quit")
    rag_context_window = []  # For RAG memory

    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        try:
            #  Query both pipelines
            rag_response = ask_rag_query(query, history=rag_context_window)
            print(f"RAG Bot: {rag_response}\n")

            #  Save to memory file
            chat_data.append({
                "user": query,
                "RAG Assistant": rag_response
            })
            with open(memory_path, "w") as f:
                json.dump(chat_data, f, indent=2)

            #  Update sliding memory
            rag_context_window.append(f"You: {query}")
            rag_context_window.append(f"RAG Bot: {rag_response}")
            rag_context_window = rag_context_window[-4:]

        except Exception as e:
            print("⚠️ Error:", e)

if __name__ == "__main__":
    main()

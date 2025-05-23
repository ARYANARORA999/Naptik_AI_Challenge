import os
import json
import re
from datetime import datetime, timedelta
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
import dateparser

#  API Key and Embedding Model
os.environ["GOOGLE_API_KEY"] = "AIzaSyBeZmM4OosHckKTTPeQW08ymisgD0uJKrs"
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#  Load structured JSONs and enrich with readable dates
def load_structured_jsons(folder="data"):
    structured_docs = []
    file_map = {
        "user_profile.json": "profile",
        "wearable_data.json": "wearable",
        "location_data.json": "location",
        "sleep_diary.json": "diary"
    }

    for fname, dtype in file_map.items():
        path = os.path.join(folder, fname)
        if not os.path.exists(path): continue
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    text = "\n".join(f"{k}: {v}" for k, v in data.items())
                    structured_docs.append(Document(page_content=text, metadata={"source": fname, "type": dtype}))
                elif isinstance(data, list):
                    for entry in data:
                        lines = [f"{k}: {v}" for k, v in entry.items() if v]
                        if "date" in entry:
                            try:
                                parsed = datetime.strptime(entry["date"], "%Y-%m-%d")
                                pretty_date = parsed.strftime("%B %d, %Y")
                                lines.append(f"pretty_date: {pretty_date}")
                            except:
                                pass
                        summary = "\n".join(lines)
                        if summary.strip():
                            structured_docs.append(Document(
                                page_content=summary,
                                metadata={
                                    "source": fname,
                                    "type": dtype,
                                    "date": entry.get("date")
                                }
                            ))
            except Exception as e:
                print(f"⚠️ Failed to load {fname}: {e}")

    return structured_docs

#  Build vector index
def build_vectorstore(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No valid document chunks to index.")
    return FAISS.from_documents(chunks, embedding)

#  Load all docs once
all_docs = load_structured_jsons()
llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature=0.4)

#  Ask query with smart filters and date memory
def ask_rag_query(query: str, history: list[str] = None) -> str:
    if history:
        query = "\n".join(history[-4:]) + "\n" + query
    q = query.lower()
    doc_filters = set()

    # --- Temporal Handling ---
    today = getattr(ask_rag_query, "last_date", None)
    parsed = dateparser.parse(query)

    if "next day" in q and today:
        inferred = today + timedelta(days=1)
        query = f"What happened on {inferred.strftime('%B %d, %Y')}?"
        q = query.lower()
        parsed = inferred
    elif "previous day" in q and today:
        inferred = today - timedelta(days=1)
        query = f"What happened on {inferred.strftime('%B %d, %Y')}?"
        q = query.lower()
        parsed = inferred
    elif "that day" in q and today:
        parsed = today

    if parsed:
        date_key = parsed.strftime("%Y-%m-%d")
        ask_rag_query.last_date = parsed
    else:
        date_key = None

    # --- Intent Detection ---
    if any(word in q for word in ["feel", "dream", "mood", "diary", "note", "vivid", "groggy", "journal"]):
        doc_filters.add("diary")
    if any(word in q for word in ["rem", "deep", "sleep", "bed", "awake", "snore", "how many hours", "sleep time"]):
        doc_filters.add("diary")
        doc_filters.add("wearable")
    elif any(word in q for word in ["steps", "calories", "caffeine", "heart rate", "distance", "energy"]):
        doc_filters.add("wearable")
        
    #  Improved location trigger
    if any(phrase in q for phrase in [
        "where was i", "was i in", "which city", "which place", "location", "country",
        "city", "whereabouts", "where did i go", "what place"
    ]):
        doc_filters.add("location")

    if any(word in q for word in ["goal", "name", "age", "gender", "profile"]):
        doc_filters.add("profile")

    print("Doc filters:", doc_filters)

    # --- Combined Filter (date + doc type) ---
    filtered_docs = all_docs
    if date_key:
        filtered_docs = [doc for doc in filtered_docs if doc.metadata.get("date") == date_key]
    if doc_filters:
        filtered_docs = [doc for doc in filtered_docs if doc.metadata.get("type") in doc_filters]

    #  If no data matched
    if not filtered_docs:
        return "I could not find any data for that day and category. Try asking about a different date or topic.\n\nSources: None"

    #  Build vectorstore from relevant docs
    temp_vs = build_vectorstore(filtered_docs)
    retriever = temp_vs.as_retriever(search_type="similarity", search_kwargs={"k": 500})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain(query)
    answer = result["result"]
    sources = [doc.metadata["source"] for doc in result["source_documents"]]
    return f"{answer}\n\nSources: {', '.join(set(sources))}"

#  Public access
def get_chat_response(query: str, history: list[str] = None) -> str:
    return ask_rag_query(query, history=history)

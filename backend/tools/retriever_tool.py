from pathlib import Path
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
import os

FAISS_PATH = Path("data/faiss_store")
INDEX_FILE = FAISS_PATH / "index.faiss"
PICKLE_FILE = FAISS_PATH / "index.pkl"

def get_retriever_tool():
    if INDEX_FILE.exists() and PICKLE_FILE.exists():
        try:
            vectordb = FAISS.load_local(
                folder_path=str(FAISS_PATH),
                embeddings=OpenAIEmbeddings(),
                allow_dangerous_deserialization=True
            )
            print("✅ Loaded existing FAISS index.")
        except Exception as e:
            print(f"❌ Error loading FAISS: {e}")
            vectordb = generate_and_save_faiss()
    else:
        vectordb = generate_and_save_faiss()

    retriever = vectordb.as_retriever(search_kwargs={"k": 1})
    return create_retriever_tool(
        retriever=retriever,
        name="smith_langchain_retriever",
        description="Retrieves info from LangChain docs.",
    )

def generate_and_save_faiss():
    print("🔄 Generating new FAISS index...")
    loader = WebBaseLoader("https://python.langchain.com/docs/tutorials/agents/")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    vectordb = FAISS.from_documents(split_docs, OpenAIEmbeddings())

    # Save to disk
    FAISS_PATH.mkdir(parents=True, exist_ok=True)
    vectordb.save_local(str(FAISS_PATH))
    print("✅ FAISS index saved.")

    return vectordb

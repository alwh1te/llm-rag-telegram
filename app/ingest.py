import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

try:
    from langchain_community.document_loaders import PyPDFLoader
    PDF_AVAILABLE = True
except Exception:
    PDF_AVAILABLE = False

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
FAISS_INDEX_DIR = os.getenv("FAISS_INDEX_DIR", "faiss_index")
DOCS_PATH = os.getenv("DOCS_PATH", "data")

def load_documents_from_folder(folder: str) -> List:
    docs = []
    folder = Path(folder)
    
    if not folder.exists():
        print(f"Folder {folder} does not exist!")
        return docs
    
    for p in folder.rglob("*"):
        if not p.is_file():
            continue
            
        if p.suffix.lower() == ".txt":
            try:
                loader = TextLoader(str(p), encoding="utf-8")
                docs += loader.load()
                print(f"Loaded: {p.name}")
            except Exception as e:
                print(f"Error loading {p.name}: {e}")
                
        elif p.suffix.lower() == ".pdf" and PDF_AVAILABLE:
            try:
                loader = PyPDFLoader(str(p))
                docs += loader.load()
                print(f"Loaded: {p.name}")
            except Exception as e:
                print(f"Error loading {p.name}: {e}")
    
    return docs

def main():
    os.makedirs(DOCS_PATH, exist_ok=True)
    
    print(f"Loading documents from {DOCS_PATH}...")
    docs = load_documents_from_folder(DOCS_PATH)
    
    if not docs:
        print(f"No documents found in {DOCS_PATH}")
        print("Please add .txt or .pdf files to the data folder")
        return

    print(f"Loaded {len(docs)} documents")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    print(f"Creating embeddings with model {EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    print("Building FAISS index...")
    faiss_index = FAISS.from_documents(chunks, embeddings)

    os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
    faiss_index.save_local(FAISS_INDEX_DIR)
    print(f"FAISS index saved to {FAISS_INDEX_DIR}")

if __name__ == "__main__":
    main()

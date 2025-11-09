# app/rag.py
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
FAISS_DIR = os.getenv("FAISS_INDEX_DIR", "faiss_index")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.0"))

def load_retriever(k: int = 3):
    if not os.path.exists(FAISS_DIR):
        raise FileNotFoundError(f"FAISS index dir '{FAISS_DIR}' not found. Run ingest.py")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(
        FAISS_DIR, 
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_qa_chain(retriever):
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=OPENAI_TEMPERATURE)
    
    template = """You are a helpful assistant that answers questions based on provided documents.

If the context contains relevant information to answer the question, use it.
If the context doesn't contain useful information or the question is general, answer as a regular AI assistant using your knowledge.

Context from documents: 
{context}

Question: {question}

Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever

def answer_question(question: str, k: int = 3):
    retriever = load_retriever(k=k)
    qa_chain, retriever_obj = create_qa_chain(retriever)
    
    answer = qa_chain.invoke(question)
    
    source_docs = retriever_obj.get_relevant_documents(question)
    srcs = [{"page_content": doc.page_content[:300], "metadata": doc.metadata} for doc in source_docs]
    
    return {"answer": answer, "sources": srcs}


def answer_question_direct(question: str, temperature: float = 0.7):
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=temperature)
    
    template = """You are a friendly and helpful AI assistant.
Answer the user's questions clearly, informatively, and politely.

Question: {question}

Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    answer = chain.invoke({"question": question})
    return {"answer": answer, "sources": []}

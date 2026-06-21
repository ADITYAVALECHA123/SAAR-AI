from backend.utils.pdf_parser import load_pdf
from backend.utils.chunking import chunk_docs
from backend.services.embeddings import get_embedding
from backend.services.vector_store import save_pdf_vectorstore
from backend.services.summarizer import summarize_text, save_summary
from backend.core.logger import logger
import os
import hashlib

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def process_pdf(file_path, user_id,  document_id, source_type="pdf"):
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are allowed")
    try:
        docs = load_pdf(file_path)
    except Exception as e:
         raise Exception(f"PDF processing failed: {str(e)}")
    if not docs:
        raise ValueError("No readable content found in PDF")
    filename = os.path.basename(file_path)
    file_hash = get_file_hash(file_path)
    for doc in docs:
        doc.metadata["document_id"]=document_id
        doc.metadata["source_type"] = source_type
        doc.metadata["source_name"] = filename
        doc.metadata["user_id"] = user_id
        doc.metadata["file_hash"] = file_hash
    logger.info(f"Loaded Pages: {len(docs)}")
    chunks = chunk_docs(docs)
    logger.info(f"Loaded Chunks: {len(chunks)}")
    embedding = get_embedding()
    save_pdf_vectorstore(chunks, embedding, user_id)
    logger.info("FAISS index saved")
    return len(docs)

def summarize_pdf(file_path, llm):
    docs = load_pdf(file_path)
    if not docs:
        return "No content found in PDF"
    chunks = chunk_docs(docs,chunk_size=2000,chunk_overlap=200)
    chunk_texts = [chunk.page_content for chunk in chunks]
    print(type(chunks[0]))
    print(chunks[0])
    summary = summarize_text("\n".join(chunk_texts),llm)
    filename = os.path.basename(file_path)
    base_name = os.path.splitext(filename)[0]
    save_summary(base_name,summary)
    return summary
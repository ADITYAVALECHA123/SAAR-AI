from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_docs(docs, chunk_size=800, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
         separators=["\n\n\n", "\n\n", "\n", ". ", " ", ""]
    )
    chunks= splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
         chunk.metadata["chunk_id"]=i+1
         chunk.metadata["chunk_size"]=len(chunk.page_content)
    return chunks

def chunk_video(transcript, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n\n", "\n\n", "\n", ". ", " ", ""])
    docs = [Document(page_content=transcript, metadata={})]
    chunks= splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"]=i+1
        chunk.metadata["chunk_size"]=len(chunk.page_content)
    return chunks
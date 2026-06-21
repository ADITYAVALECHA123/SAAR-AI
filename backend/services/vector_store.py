from langchain_community.vectorstores import FAISS
from backend.core.logger import logger
import os

def get_user_vector_path(user_id, vector_type):
    return os.path.join("vector_store", "users", str(user_id), vector_type)

def save_vectorstore(docs, embedding, user_id, vector_type):
    DB_PATH = get_user_vector_path(user_id, vector_type)
    os.makedirs(DB_PATH, exist_ok=True)
    index_file = os.path.join(DB_PATH, "index.faiss")
    if os.path.exists(index_file):
        db = FAISS.load_local(DB_PATH,embedding,allow_dangerous_deserialization=True)
        db.add_documents(docs)
        logger.info(
            f"Documents added to existing"
            f"{vector_type} vector store")
    else:
        db = FAISS.from_documents(docs, embedding)
        logger.info(f"New {vector_type} Vector store created")
    db.save_local(DB_PATH)
    logger.info(
        f"{vector_type} vector store saved "
        f"for user {user_id}")

def load_vectorstore(embedding, user_id, vector_type):
    DB_PATH = get_user_vector_path(user_id, vector_type)
    index_file = os.path.join(DB_PATH, "index.faiss")
    if not os.path.exists(index_file):
        logger.warning(
            f"{vector_type} Index not Found"
            f"for user {user_id}"
        )
        return None
    logger.info(
        f"{vector_type} Vector store loaded"
        f"for user{user_id}")
    return FAISS.load_local(DB_PATH,embedding,allow_dangerous_deserialization=True)

def save_pdf_vectorstore(docs,embedding,user_id):
    save_vectorstore(docs=docs, embedding=embedding, user_id=user_id, vector_type="pdf_index")


def load_pdf_vectorstore(embedding,user_id):
    return load_vectorstore(embedding=embedding, user_id=user_id,vector_type="pdf_index")

def save_video_vectorstore(docs,embedding,user_id):
    save_vectorstore(docs=docs, embedding=embedding, user_id=user_id, vector_type="video_index")


def load_video_vectorstore(embedding,user_id):
    return load_vectorstore(embedding=embedding, user_id=user_id,vector_type="video_index")

def save_research_vectorstore(docs,embedding,user_id):
    save_vectorstore(docs=docs, embedding=embedding, user_id=user_id, vector_type="research_index")


def load_research_vectorstore(embedding,user_id):
    return load_vectorstore(embedding=embedding, user_id=user_id,vector_type="research_index")

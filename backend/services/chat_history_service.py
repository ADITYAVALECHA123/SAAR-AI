from sqlalchemy.orm import Session
from backend.db.database import SessionLocal
from backend.models.chat_session import ChatSession
from backend.models.chat_message import ChatMessage

def create_chat_session(user_id,title="New Chat"):
    db = SessionLocal()
    try:
        session = ChatSession(user_id=user_id,title=title)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    finally:
        db.close()

def save_chat_message(session_id,role,content):
    db = SessionLocal()
    try:
        message = ChatMessage(session_id=session_id,role=role,content=content)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    finally:
        db.close()

def get_chat_messages(session_id):
    db = SessionLocal()
    try:
        messages = (db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all())
        return [
            {
                "role": m.role,
                "content": m.content
            }
            for m in messages
        ]
    finally:
        db.close()

def get_user_chat_sessions(user_id):
    db = SessionLocal()
    try:
        sessions = (db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.updated_at.desc()).all())
        return sessions
    finally:
        db.close()

def get_chat_session(session_id):
    db = SessionLocal()
    try:
        return (
            db.query(ChatSession).filter(ChatSession.id == session_id).first())
    finally:
        db.close()
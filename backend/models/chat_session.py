from sqlalchemy import Column,Integer,String, ForeignKey,DateTime
from datetime import datetime
from backend.db.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),index=True)
    title = Column(String,default="New Chat")
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
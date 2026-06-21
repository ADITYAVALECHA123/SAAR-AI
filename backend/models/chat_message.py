from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Text
from datetime import datetime
from backend.db.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer,primary_key=True, index=True)
    session_id = Column(Integer,ForeignKey("chat_sessions.id"),index=True)
    role = Column(String,nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)
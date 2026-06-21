from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from backend.db.database import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    file_hash = Column(String, nullable=True, index=True)
    file_size = Column(Integer, nullable=True)
    page_count = Column(Integer, nullable=True)
    indexed_status = Column(String,default="processing", nullable=False)
    upload_date = Column(DateTime,default=datetime.utcnow, nullable=False)
    source_type = Column(String, nullable=True)
    external_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    authors = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
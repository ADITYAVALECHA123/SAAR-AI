from sqlalchemy import Column,Integer,String,Float,ForeignKey
from backend.db.database import Base

class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),unique=True, index=True, nullable=False)
    selected_model = Column(String,default="llama-3.3-70b-versatile", nullable=False)
    chunk_size = Column(Integer,default=512)
    top_k = Column(Integer,default=5)
    temperature = Column(Float,default=0.3)
    theme = Column(String,default="Dark (default)")
    font_size = Column(String,default="Medium")
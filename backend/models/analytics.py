from sqlalchemy import Column,Integer,Float,String,ForeignKey,DateTime
from datetime import datetime
from backend.db.database import Base

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=True, index=True)
    query = Column(String,nullable=True)
    source = Column(String,nullable=True)
    response_time = Column(Float, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow, nullable=False, index=True)
    model_name = Column(String,nullable=True, index=True)
    query_type = Column(String,nullable=True, index=True)
    tokens_used = Column(Integer,nullable=True)
    status = Column(String,default="success", index=True)
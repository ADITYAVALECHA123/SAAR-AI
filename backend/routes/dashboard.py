from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session
from backend.dependency.dependencies import get_db
from backend.models.analytics import QueryLog
from backend.models.document import Document
from sqlalchemy import func

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_dashboard_stats(user_id: int, db: Session = Depends(get_db)):
    print("Dashboard API Called")
    print("Current User:", user_id)
    total_queries = db.query(QueryLog).filter(QueryLog.user_id == user_id).count()
    avg_response = db.query(func.avg(QueryLog.response_time))\
        .filter(QueryLog.user_id == user_id).scalar() or 0
    total_docs = db.query(Document).filter(Document.user_id == user_id).count()
    print("DB PATH:", db.bind.url)
    return {
        "documents": total_docs,
        "queries": total_queries,
        "avg_response": round(avg_response, 2),
        "accuracy": 94.2
    }
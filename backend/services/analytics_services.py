from backend.db.database import SessionLocal
from backend.models.analytics import QueryLog
from sqlalchemy import func
from datetime import datetime, timedelta
from collections import Counter

def get_analytics(user_id):
    db = SessionLocal()
    try:
        total_queries = (db.query(QueryLog).filter(QueryLog.user_id == user_id).count())
        avg_response = (db.query(func.avg(QueryLog.response_time)).filter(QueryLog.user_id == user_id).scalar() or 0)
        last_week = datetime.utcnow() - timedelta(days=7)
        recent_queries_objects = (db.query(QueryLog).filter(QueryLog.created_at >= last_week, QueryLog.user_id == user_id).order_by(QueryLog.created_at.desc()).all())
        topic_counter = Counter()
        for item in recent_queries_objects:
            if item.query:
                words = item.query.lower().split()
                for word in words:
                    if len(word) > 3:
                        topic_counter[word] += 1
        top_topics = [{
            "topics":topic,
            "count":count
        }
        for topic, count in topic_counter.most_common(6)]
        source_counts_raw = (db.query(QueryLog.source,func.count(QueryLog.id)).filter(QueryLog.user_id==user_id).group_by(QueryLog.source).all())
        source_counts = [{"source": source, "count": count} for source, count in source_counts_raw]
        daily_counts_raw = (db.query(func.date(QueryLog.created_at),func.count(QueryLog.id)).filter(QueryLog.user_id==user_id).group_by(func.date(QueryLog.created_at)).all())
        daily_counts = [{"date": str(date), "count": count} for date, count in daily_counts_raw]
        recent_queries = [{
            "id":q.id,
            "query":q.query,
            "source":q.source,
            "response_timw":q.response_time,
            "created_at": q.created_at.isoformat()
            if q.created_at else None
        } for q in recent_queries_objects]
        return {
            "total_queries": total_queries,
            "avg_response": round(avg_response, 2),
            "recent_queries": recent_queries,
            "source_counts": source_counts,
            "daily_counts": daily_counts,
            "top_topics": top_topics
    }
    finally:
        db.close()
    
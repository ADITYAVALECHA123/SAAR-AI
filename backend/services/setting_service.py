from backend.db.database import SessionLocal
from backend.models.setting import UserSettings

def save_user_settings(user_id, data):
    db = SessionLocal()
    try:
        settings = db.query(UserSettings).filter(
            UserSettings.user_id == user_id
        ).first()
        if not settings:
            db.add(settings)
        for key, value in data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        db.commit()
        db.refresh(settings)
        return{
            "selected_model": settings.selected_model, 
            "chunk_size": settings.chunk_size,
            "top_k":settings.top_k,
            "temperature": settings.temperature,
            "theme": settings.theme,
            "font_size": settings.font_size}
    finally:
        db.close()

def load_user_settings(user_id):
    db = SessionLocal()
    try:
        settings = db.query(UserSettings).filter(
            UserSettings.user_id == user_id
        ).first()
        db.close()
        if not settings:
            settings = UserSettings(user_id = user_id)
            db.add(settings)
            db.commit()
            db.refresh(settings)
        return {
            "selected_model": settings.selected_model,
            "chunk_size": settings.chunk_size,
            "top_k": settings.top_k,
            "temperature": settings.temperature,
            "theme": settings.theme,
            "font_size": settings.font_size
        }
    finally:
        db.close()
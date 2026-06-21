from backend.db.database import engine, Base
from backend.models.user import User
from backend.models.document import Document
from backend.models.analytics import QueryLog
from backend.models.setting import UserSettings
from backend.core.logger import logger

Base.metadata.create_all(bind=engine)

logger.info("Database created successfully")
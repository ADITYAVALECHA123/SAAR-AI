from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from backend.core.config import settings
from backend.core.logger import logger

ALGORITHM=settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing from environment variables")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except JWTError as e:
        logger.error(f"JWT Verification Failed: {str(e)}")
        return None
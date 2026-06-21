from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.security.jwt_handler import verify_token
from backend.models.user import User
from backend.dependency.dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = (db.query(User).filter(User.id == int(user_id)).first())
    if not user:
        raise HTTPException(status_code=404,detail="Invalid authentication credentials")
    return user
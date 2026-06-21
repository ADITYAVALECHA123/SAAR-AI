from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user_schema import UserCreate, UserLogin
from backend.security.hashing import hash_password, verify_password
from backend.security.jwt_handler import create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer
from backend.dependency.dependencies import get_db
from datetime import datetime
from backend.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    email = user.email.strip().lower()
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        full_name=user.full_name,
        email=email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    email = user.email.strip().lower()
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if db_user.provider == "google":
        raise HTTPException(status_code=400,detail="Please login with Google")
    if not db_user.is_active:
        raise HTTPException(status_code=403,detail="Account is disabled")
    if not verify_password(user.password,db_user.hashed_password):
        db_user.failed_login_attempts +=1
        db.commit()
        raise HTTPException(status_code=401,detail="Invalid credentials")
    db_user.failed_login_attempts = 0
    db_user.last_login = datetime.utcnow()
    db.commit()
    token = create_access_token({"sub": str(db_user.id)})
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": db_user.id,
            "name": db_user.full_name,
            "email": db_user.email
        }
    }

@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return {
        "message": "Access granted",
        "user": payload
    }


from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    SECRET_KEY: str
    Hf_Token: str
    GROQ_API_KEY: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    ALGORITHM: str = "HS256"
    CORE: str 

    class Config:
        env_file = ".env"
        case_sensitive=True

settings = Settings()
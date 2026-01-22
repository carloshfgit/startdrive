from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GoDrive"
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str
    DATABASE_URL: str

    STRIPE_API_KEY: str 
    STRIPE_WEBHOOK_SECRET: str 
    PLATFORM_FEE_PERCENT: float = 0.15

    # --- NOVO ---
    # Default para localhost caso rode fora do docker
    REDIS_URL: str = "redis://localhost:6379" 

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore" 

settings = Settings()
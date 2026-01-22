# app/core/security.py
from datetime import datetime, timedelta, timezone # <--- Adicione o timezone aqui
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.infrastructure.config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    # Cria a data atual já com a informação de fuso horário UTC
    now = datetime.now(timezone.utc) # <--- Correção aqui
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # O .timestamp() do Python converte corretamente datas aware para Unix Timestamp
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
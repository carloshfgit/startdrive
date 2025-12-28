from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash

router = APIRouter()
user_repo = UserRepository()

# Dependência para pegar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário (Aluno ou Instrutor).
    """
    # 1. Verifica se email já existe
    user = user_repo.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="O email informado já está cadastrado no sistema."
        )
    
    # 2. Criptografa a senha
    hashed_password = get_password_hash(user_in.password)
    
    # 3. Salva no banco
    return user_repo.create(db=db, user=user_in, hashed_password=hashed_password)
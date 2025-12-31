from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash
from app.api import deps
from app.repositories.ride_repository import RideRepository 
from app.models.user import User


router = APIRouter()
user_repo = UserRepository()
ride_repo = RideRepository()

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
    user = user_repo.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="O email informado já está cadastrado no sistema."
        )
    
    hashed_password = get_password_hash(user_in.password)
    user = user_repo.create(db=db, user=user_in, hashed_password=hashed_password)
    
    # Ajuste manual para o schema responder sem erro
    user.has_pending_reviews = False 
    return user
    
@router.get("/me", response_model=UserResponse)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retorna os dados do usuário logado e verifica pendências.
    """
    # Verifica se existem avaliações pendentes
    pending_rides = ride_repo.get_pending_reviews_for_user(db, user_id=current_user.id)
    
    # Injeta a informação no objeto antes de retornar (o Pydantic lê isso)
    current_user.has_pending_reviews = len(pending_rides) > 0
    
    return current_user
# app/api/v1/endpoints/reviews.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.ride import Ride, RideStatus
from app.schemas.review import ReviewCreate, ReviewResponse, RatingSummary
from app.repositories.review_repository import ReviewRepository

router = APIRouter()
repo = ReviewRepository()

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Cria uma avaliação para uma aula finalizada.
    O sistema detecta automaticamente se você é o Aluno (e está avaliando o Instrutor)
    ou vice-versa.
    """
    # 1. Buscar a aula
    ride = db.query(Ride).filter(Ride.id == review_in.ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")

    # 2. Validar Participação
    if current_user.id not in [ride.student_id, ride.instructor_id]:
        raise HTTPException(status_code=403, detail="Você não participou desta aula.")

    # 3. Validar Status da Aula
    if ride.status != RideStatus.COMPLETED:
        raise HTTPException(
            status_code=400, 
            detail="Você só pode avaliar aulas que foram finalizadas (COMPLETED)."
        )

    # 4. Definir quem é o Avaliado (O "Outro")
    if current_user.id == ride.student_id:
        reviewee_id = ride.instructor_id
    else:
        reviewee_id = ride.student_id

    # 5. Evitar Duplicidade
    if repo.get_existing_review(db, ride_id=ride.id, reviewer_id=current_user.id):
        raise HTTPException(status_code=409, detail="Você já avaliou esta aula.")

    # 6. Salvar
    new_review = repo.create(
        db=db, 
        reviewer_id=current_user.id, 
        reviewee_id=reviewee_id, 
        review_in=review_in
    )
    
    # Injetar nome para resposta (opcional)
    new_review.reviewer_name = current_user.full_name
    
    return new_review

@router.get("/user/{user_id}", response_model=List[ReviewResponse])
def list_user_reviews(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Lista as avaliações que um usuário recebeu.
    """
    reviews = repo.get_by_user(db, user_id=user_id)
    # Popula o nome do avaliador manualmente (ou via relacionamento eager load)
    for r in reviews:
        r.reviewer_name = r.reviewer.full_name
    return reviews

@router.get("/user/{user_id}/summary", response_model=RatingSummary)
def get_user_rating_summary(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retorna a média de estrelas e o total de avaliações de um usuário.
    """
    return repo.get_stats_by_user(db, user_id=user_id)
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.instructor import InstructorProfile
from app.schemas.ride import RideCreate, RideResponse
from app.repositories.ride_repository import RideRepository

router = APIRouter()
ride_repo = RideRepository()

@router.post("/", response_model=RideResponse, status_code=status.HTTP_201_CREATED)
def create_ride(
    ride_in: RideCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Cria uma solicitação de aula (Booking).
    Status inicial: PENDING_PAYMENT.
    """
    # 1. Busca o instrutor para pegar o preço atual
    instructor = db.query(InstructorProfile).filter(InstructorProfile.id == ride_in.instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado.")
    
    # 2. Define o preço (se o instrutor não tiver preço configurado, usa um fallback ou erro)
    price = instructor.hourly_rate if instructor.hourly_rate else 0.0
    
    # 3. Cria a reserva
    # TODO (Refinamento): Verificar se o horário bate com a Availability do instrutor
    return ride_repo.create(db=db, student_id=current_user.id, ride_in=ride_in, price=price)

@router.get("/", response_model=List[RideResponse])
def read_my_rides(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Lista as aulas do usuário logado.
    Funciona tanto para Aluno quanto para Instrutor.
    """
    if current_user.user_type == "instructor":
        # Se for instrutor, busca pelo perfil
        if not current_user.instructor_profile:
            return []
        return ride_repo.get_by_instructor(db, instructor_id=current_user.instructor_profile.id)
    else:
        # Se for aluno, busca pelo ID de usuário
        return ride_repo.get_by_student(db, student_id=current_user.id)
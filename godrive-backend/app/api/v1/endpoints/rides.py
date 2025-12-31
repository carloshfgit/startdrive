from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.instructor import InstructorProfile
from app.schemas.ride import RideCreate, RideResponse
from app.repositories.ride_repository import RideRepository
from app.services.availability_service import AvailabilityService  # [Novo Import]

router = APIRouter()
ride_repo = RideRepository()
availability_service = AvailabilityService()  # [Instância do Serviço]

@router.post("/", response_model=RideResponse, status_code=status.HTTP_201_CREATED)
def create_ride(
    ride_in: RideCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Cria uma solicitação de aula (Booking).
    Valida se a data é futura e se o instrutor possui disponibilidade.
    """
    # 1. Validação Temporal: Não permitir agendamento no passado
    # Garante que ambos estejam em UTC para comparação correta
    now = datetime.now(timezone.utc)
    if ride_in.scheduled_at < now:
        raise HTTPException(
            status_code=400,
            detail="Não é possível agendar aulas para uma data/hora no passado."
        )

    # 2. Validação de Disponibilidade: O instrutor está livre neste horário?
    available_slots = availability_service.get_available_slots(
        db=db,
        instructor_id=ride_in.instructor_id,
        query_date=ride_in.scheduled_at.date()
    )
    
    # Extrai o horário (time) da requisição para comparar com os slots
    request_time = ride_in.scheduled_at.time()
    
    if request_time not in available_slots:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O instrutor não está disponível neste horário."
        )

    # 3. Busca o instrutor para pegar o preço atual
    instructor = db.query(InstructorProfile).filter(InstructorProfile.id == ride_in.instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado.")
    
    # 4. Define o preço
    price = instructor.hourly_rate if instructor.hourly_rate else 0.0
    
    # 5. Cria a reserva
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
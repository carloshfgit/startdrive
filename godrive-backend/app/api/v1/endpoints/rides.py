from typing import List
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.instructor import InstructorProfile
from app.models.ride import Ride, RideStatus
from app.schemas.ride import RideCreate, RideResponse
from app.repositories.ride_repository import RideRepository
from app.services.availability_service import AvailabilityService
from app.services.socket_service import socket_manager # [Novo Import] para notificar o app
from app.schemas.ride import RideCreate, RideResponse, RideStart # <--- Importe RideStart
from app.utils.geo import haversine # <--- Importe a função

router = APIRouter()
ride_repo = RideRepository()
availability_service = AvailabilityService()

@router.post("/", response_model=RideResponse, status_code=status.HTTP_201_CREATED)
def create_ride(
    ride_in: RideCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Cria uma solicitação de aula (Booking).
    """
    # 1. Validação Temporal
    now = datetime.now(timezone.utc)
    if ride_in.scheduled_at < now:
        raise HTTPException(
            status_code=400,
            detail="Não é possível agendar aulas para uma data/hora no passado."
        )

    # 2. Validação de Disponibilidade
    available_slots = availability_service.get_available_slots(
        db=db,
        instructor_id=ride_in.instructor_id,
        query_date=ride_in.scheduled_at.date()
    )
    request_time = ride_in.scheduled_at.time()
    if request_time not in available_slots:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O instrutor não está disponível neste horário."
        )

    # 3. Busca o instrutor e Preço
    instructor = db.query(InstructorProfile).filter(InstructorProfile.id == ride_in.instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado.")
    
    price = instructor.hourly_rate if instructor.hourly_rate else 0.0
    
    return ride_repo.create(db=db, student_id=current_user.id, ride_in=ride_in, price=price)

@router.get("/", response_model=List[RideResponse])
def read_my_rides(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Lista as aulas do usuário logado.
    """
    if current_user.user_type == "instructor":
        if not current_user.instructor_profile:
            return []
        return ride_repo.get_by_instructor(db, instructor_id=current_user.instructor_profile.id)
    else:
        return ride_repo.get_by_student(db, student_id=current_user.id)


@router.patch("/{ride_id}/finish", response_model=RideResponse)
async def finish_ride(
    ride_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Instrutor finaliza a aula.
    Muda status para COMPLETED e encerra rastreamento.
    """
    ride = ride_repo.get_by_id(db, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")

    # 1. Apenas o Instrutor pode finalizar
    if ride.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o instrutor responsável pode finalizar a aula.")

    # 2. Validação de Status
    if ride.status != RideStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="A aula não está em andamento.")

    # 3. Atualização de Estado
    ride.status = RideStatus.COMPLETED
    ride.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ride)

    # 4. Notificação Final via WebSocket
    await socket_manager.broadcast_location(ride.id, {"type": "RIDE_FINISHED", "message": "A aula foi finalizada."})
    
    # Opcional: Forçar desconexão dos sockets desta sala
    # socket_manager.close_room(ride.id) 

@router.patch("/{ride_id}/start", response_model=RideResponse)
async def start_ride(
    ride_id: int,
    start_in: RideStart, # <--- Novo Payload
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Instrutor inicia a aula. Valida se ele está próximo ao local de encontro.
    """
    ride = ride_repo.get_by_id(db, ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")

    # 1. Validação de Autorização (já existente)
    if ride.instructor_id != current_user.id:
         # Verificação simplificada assumindo ID User = ID Instrutor
         # (Se tiver ID separado, ajustar conforme seu modelo)
         raise HTTPException(status_code=403, detail="Apenas o instrutor responsável pode iniciar a aula.")

    # 2. Validação de Status (já existente)
    if ride.status != RideStatus.SCHEDULED:
        raise HTTPException(status_code=400, detail=f"Não é possível iniciar uma aula com status '{ride.status}'.")

    # 3. VALIDAÇÃO GEO-FENCING (NOVO)
    # Tolerância de 150 metros (0.15 km)
    MAX_DISTANCE_KM = 0.15
    
    # Verifica se a aula tem local de encontro definido (retrocompatibilidade)
    if ride.pickup_latitude and ride.pickup_longitude:
        distance = haversine(
            ride.pickup_latitude, ride.pickup_longitude,
            start_in.latitude, start_in.longitude
        )
        
        if distance > MAX_DISTANCE_KM:
            raise HTTPException(
                status_code=400, 
                detail=f"Você está muito longe do aluno ({int(distance*1000)}m). Aproxime-se do local de encontro para iniciar."
            )
    
    # 4. Atualização de Estado
    ride.status = RideStatus.IN_PROGRESS
    ride.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ride)

    # 5. Notificação via WebSocket
    await socket_manager.broadcast_location(ride.id, {"type": "RIDE_STARTED", "message": "A aula começou!"})

    return ride
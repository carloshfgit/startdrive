from typing import List
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.interface.api import deps
from app.infrastructure.db.models.user import User
from app.infrastructure.db.models.instructor import InstructorProfile
from app.infrastructure.db.models.ride import Ride, RideStatus
from app.interface.api.schemas.ride import RideCreate, RideResponse
from app.infrastructure.repositories.ride_repository import RideRepository
from app.application.use_cases.availability.availability_service import AvailabilityService
from app.infrastructure.external.socket_service import socket_manager # [Novo Import] para notificar o app
from app.interface.api.schemas.ride import RideCreate, RideResponse, RideStart # <--- Importe RideStart
from app.utils.geo import haversine # <--- Importe a função

# --- Clean Architecture Imports ---
from app.application.use_cases.criar_agendamento import (
    CriarAgendamentoUseCase, 
    CriarAgendamentoInput,
)
from app.infrastructure.repositories.adapters import (
    RideRepositoryAdapter,
    InstructorRepositoryAdapter,
    AvailabilityServiceAdapter,
)
from app.domain.exceptions.ride import (
    RideScheduleInPastException,
    SlotNotAvailableException,
)
from app.domain.exceptions.instructor import InstructorNotFoundException

router = APIRouter()
ride_repo = RideRepository()
availability_service = AvailabilityService()


# --- Factory para Injeção de Dependência do Use Case ---
def get_criar_agendamento_use_case(
    db: Session = Depends(deps.get_db)
) -> CriarAgendamentoUseCase:
    """
    Factory que cria o Use Case com todas as dependências injetadas.
    Os adapters envolvem os repositories legados.
    """
    return CriarAgendamentoUseCase(
        ride_repository=RideRepositoryAdapter(db),
        instructor_repository=InstructorRepositoryAdapter(db),
        availability_service=AvailabilityServiceAdapter(db),
    )

@router.post("/", response_model=RideResponse, status_code=status.HTTP_201_CREATED)
def create_ride(
    ride_in: RideCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    use_case: CriarAgendamentoUseCase = Depends(get_criar_agendamento_use_case),
):
    """
    Cria uma solicitação de aula (Booking).
    
    Refatorado para Clean Architecture:
    - Controller apenas recebe request e delega para Use Case
    - Lógica de negócio está em CriarAgendamentoUseCase
    - Exceções de domínio são mapeadas para HTTP status codes
    """
    try:
        result = use_case.execute(CriarAgendamentoInput(
            student_id=current_user.id,
            instructor_id=ride_in.instructor_id,
            scheduled_at=ride_in.scheduled_at,
            pickup_latitude=ride_in.pickup_latitude,
            pickup_longitude=ride_in.pickup_longitude,
        ))
        
        # Busca o modelo do banco para retornar no formato RideResponse
        # (o Use Case retorna entity, precisamos do model para o schema)
        db_ride = db.query(Ride).filter(Ride.id == result.ride.id).first()
        return db_ride
        
    except RideScheduleInPastException:
        raise HTTPException(
            status_code=400,
            detail="Não é possível agendar aulas para uma data/hora no passado."
        )
    except InstructorNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SlotNotAvailableException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O instrutor não está disponível neste horário."
        )

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
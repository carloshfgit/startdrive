"""
Use Case: Criar Agendamento

Caso de uso para criar um novo agendamento de aula de direção.
Contém todas as regras de negócio relacionadas ao agendamento.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from app.domain.entities.ride import RideEntity, RideStatus
from app.domain.interfaces.ride_repository import IRideRepository
from app.domain.interfaces.instructor_repository import IInstructorRepository
from app.domain.interfaces.availability_service import IAvailabilityService
from app.domain.exceptions.ride import (
    RideScheduleInPastException,
    SlotNotAvailableException,
)
from app.domain.exceptions.instructor import InstructorNotFoundException


@dataclass
class CriarAgendamentoInput:
    """
    Dados de entrada para o caso de uso.
    
    Attributes:
        student_id: ID do aluno que está agendando.
        instructor_id: ID do instrutor escolhido.
        scheduled_at: Data e hora do agendamento.
        pickup_latitude: Latitude do ponto de encontro (opcional).
        pickup_longitude: Longitude do ponto de encontro (opcional).
    """
    student_id: int
    instructor_id: int
    scheduled_at: datetime
    pickup_latitude: Optional[float] = None
    pickup_longitude: Optional[float] = None


@dataclass
class CriarAgendamentoOutput:
    """
    Dados de saída do caso de uso.
    
    Attributes:
        ride: A entidade de aula criada.
    """
    ride: RideEntity


class CriarAgendamentoUseCase:
    """
    Caso de Uso: Criar um agendamento de aula.
    
    Regras de Negócio:
    1. Não é possível agendar no passado
    2. O instrutor deve existir
    3. O horário deve estar disponível
    4. O preço é definido pelo hourly_rate do instrutor
    
    Example:
        >>> use_case = CriarAgendamentoUseCase(ride_repo, instructor_repo, availability_svc)
        >>> result = use_case.execute(CriarAgendamentoInput(...))
        >>> print(result.ride.id)
    """
    
    def __init__(
        self,
        ride_repository: IRideRepository,
        instructor_repository: IInstructorRepository,
        availability_service: IAvailabilityService,
    ):
        """
        Inicializa o caso de uso com suas dependências.
        
        Args:
            ride_repository: Repositório de aulas (interface).
            instructor_repository: Repositório de instrutores (interface).
            availability_service: Serviço de disponibilidade (interface).
        """
        self._ride_repo = ride_repository
        self._instructor_repo = instructor_repository
        self._availability_svc = availability_service
    
    def execute(self, input_data: CriarAgendamentoInput) -> CriarAgendamentoOutput:
        """
        Executa o caso de uso de criação de agendamento.
        
        Args:
            input_data: Dados de entrada para o agendamento.
            
        Returns:
            CriarAgendamentoOutput com a aula criada.
            
        Raises:
            RideScheduleInPastException: Se a data/hora está no passado.
            InstructorNotFoundException: Se o instrutor não existe.
            SlotNotAvailableException: Se o horário não está disponível.
        """
        # 1. Validação Temporal - Não pode agendar no passado
        now = datetime.now(timezone.utc)
        if input_data.scheduled_at < now:
            raise RideScheduleInPastException()
        
        # 2. Buscar Instrutor - Deve existir
        instructor = self._instructor_repo.get_by_id(input_data.instructor_id)
        if not instructor:
            raise InstructorNotFoundException(input_data.instructor_id)
        
        # 3. Validar Disponibilidade - Horário deve estar livre
        available_slots = self._availability_svc.get_available_slots(
            instructor_id=input_data.instructor_id,
            query_date=input_data.scheduled_at.date()
        )
        request_time = input_data.scheduled_at.time()
        if request_time not in available_slots:
            raise SlotNotAvailableException(
                input_data.instructor_id, 
                request_time.isoformat()
            )
        
        # 4. Criar Entidade de Aula
        ride = RideEntity(
            id=0,  # Será preenchido pelo repository
            student_id=input_data.student_id,
            instructor_id=input_data.instructor_id,
            scheduled_at=input_data.scheduled_at,
            price=instructor.hourly_rate if instructor.hourly_rate else 0.0,
            status=RideStatus.PENDING,
            pickup_latitude=input_data.pickup_latitude,
            pickup_longitude=input_data.pickup_longitude,
        )
        
        # 5. Persistir via Repository
        created_ride = self._ride_repo.create(ride)
        
        return CriarAgendamentoOutput(ride=created_ride)

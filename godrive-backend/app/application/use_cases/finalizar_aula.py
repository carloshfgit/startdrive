"""
Use Case: Finalizar Aula

Caso de uso para instrutor finalizar uma aula em andamento.
"""
from dataclasses import dataclass
from datetime import datetime, timezone

from app.domain.entities.ride import RideEntity, RideStatus
from app.domain.interfaces.ride_repository import IRideRepository
from app.domain.exceptions.ride import (
    RideNotFoundException,
    RideStatusTransitionException,
    UnauthorizedRideActionException,
)


@dataclass
class FinalizarAulaInput:
    """Dados de entrada para finalizar aula."""
    ride_id: int
    instructor_user_id: int


@dataclass
class FinalizarAulaOutput:
    """Dados de saída após finalizar aula."""
    ride: RideEntity


class FinalizarAulaUseCase:
    """
    Caso de Uso: Finalizar uma aula em andamento.
    
    Regras de Negócio:
    1. A aula deve existir
    2. Apenas o instrutor responsável pode finalizar
    3. A aula deve estar com status IN_PROGRESS
    """
    
    def __init__(self, ride_repository: IRideRepository):
        self._ride_repo = ride_repository
    
    def execute(self, input_data: FinalizarAulaInput) -> FinalizarAulaOutput:
        # 1. Buscar aula
        ride = self._ride_repo.get_by_id(input_data.ride_id)
        if not ride:
            raise RideNotFoundException(input_data.ride_id)
        
        # 2. Verificar autorização
        if ride.instructor_id != input_data.instructor_user_id:
            raise UnauthorizedRideActionException(
                action="finalizar",
                user_id=input_data.instructor_user_id,
                ride_id=input_data.ride_id
            )
        
        # 3. Verificar status
        if not ride.can_be_finished():
            raise RideStatusTransitionException(
                current_status=ride.status.value,
                target_status=RideStatus.COMPLETED.value
            )
        
        # 4. Finalizar aula
        ride.finish()
        updated_ride = self._ride_repo.update(ride)
        
        return FinalizarAulaOutput(ride=updated_ride)

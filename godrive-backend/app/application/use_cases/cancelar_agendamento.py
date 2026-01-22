"""
Use Case: Cancelar Agendamento

Caso de uso para cancelar um agendamento de aula.
Aplica regra de multa conforme política de cancelamento.
"""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

from app.domain.entities.ride import RideEntity, RideStatus
from app.domain.interfaces.ride_repository import IRideRepository
from app.domain.exceptions.ride import (
    RideNotFoundException,
    RideStatusTransitionException,
    UnauthorizedRideActionException,
)


@dataclass
class CancelarAgendamentoInput:
    """Dados de entrada para cancelar agendamento."""
    ride_id: int
    user_id: int  # Pode ser aluno ou instrutor


@dataclass
class CancelarAgendamentoOutput:
    """Dados de saída após cancelar agendamento."""
    ride: RideEntity
    refund_percentage: float  # 100% ou 50% conforme regra
    penalty_applied: bool


class CancelarAgendamentoUseCase:
    """
    Caso de Uso: Cancelar um agendamento de aula.
    
    Regras de Negócio (conforme PROJECT_GUIDELINES.md):
    1. A aula deve existir
    2. Apenas participantes (aluno ou instrutor) podem cancelar
    3. A aula deve estar com status PENDING ou SCHEDULED
    4. IF tempo_para_aula > 24h THEN reembolso = 100%
    5. IF tempo_para_aula < 24h THEN multa = 50%
    """
    
    # Limite para reembolso total
    FULL_REFUND_HOURS = 24
    PENALTY_PERCENTAGE = 0.50
    
    def __init__(self, ride_repository: IRideRepository):
        self._ride_repo = ride_repository
    
    def execute(self, input_data: CancelarAgendamentoInput) -> CancelarAgendamentoOutput:
        # 1. Buscar aula
        ride = self._ride_repo.get_by_id(input_data.ride_id)
        if not ride:
            raise RideNotFoundException(input_data.ride_id)
        
        # 2. Verificar autorização (aluno ou instrutor)
        is_student = ride.student_id == input_data.user_id
        is_instructor = ride.instructor_id == input_data.user_id
        
        if not (is_student or is_instructor):
            raise UnauthorizedRideActionException(
                action="cancelar",
                user_id=input_data.user_id,
                ride_id=input_data.ride_id
            )
        
        # 3. Verificar status
        if not ride.can_be_cancelled():
            raise RideStatusTransitionException(
                current_status=ride.status.value,
                target_status=RideStatus.CANCELLED.value
            )
        
        # 4. Calcular reembolso/multa
        now = datetime.now(timezone.utc)
        time_until_ride = ride.scheduled_at - now
        hours_until_ride = time_until_ride.total_seconds() / 3600
        
        if hours_until_ride >= self.FULL_REFUND_HOURS:
            refund_percentage = 1.0  # 100%
            penalty_applied = False
        else:
            refund_percentage = 1.0 - self.PENALTY_PERCENTAGE  # 50%
            penalty_applied = True
        
        # 5. Cancelar aula
        ride.cancel()
        updated_ride = self._ride_repo.update(ride)
        
        return CancelarAgendamentoOutput(
            ride=updated_ride,
            refund_percentage=refund_percentage,
            penalty_applied=penalty_applied
        )

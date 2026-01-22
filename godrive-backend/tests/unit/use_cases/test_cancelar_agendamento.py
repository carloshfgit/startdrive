"""
Testes unitários para CancelarAgendamentoUseCase.
"""
import pytest
from datetime import datetime, timezone, timedelta

from app.application.use_cases.cancelar_agendamento import (
    CancelarAgendamentoUseCase,
    CancelarAgendamentoInput,
)
from app.domain.entities.ride import RideEntity, RideStatus
from app.domain.exceptions.ride import (
    RideNotFoundException,
    RideStatusTransitionException,
    UnauthorizedRideActionException,
)


class TestCancelarAgendamentoUseCase:
    """Testes para o caso de uso Cancelar Agendamento."""
    
    def test_cancelar_com_24h_antecedencia_reembolso_total(self, ride_repository):
        """Deve dar 100% de reembolso se cancelar com mais de 24h."""
        # Arrange
        future_ride = RideEntity(
            id=1,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc) + timedelta(hours=48),  # 48h no futuro
            price=100.0,
            status=RideStatus.SCHEDULED,
        )
        ride_repository.add_ride(future_ride)
        
        use_case = CancelarAgendamentoUseCase(ride_repository)
        input_data = CancelarAgendamentoInput(ride_id=1, user_id=100)
        
        # Act
        result = use_case.execute(input_data)
        
        # Assert
        assert result.ride.status == RideStatus.CANCELLED
        assert result.refund_percentage == 1.0  # 100%
        assert result.penalty_applied is False
    
    def test_cancelar_com_menos_24h_aplica_multa(self, ride_repository):
        """Deve aplicar 50% de multa se cancelar com menos de 24h."""
        # Arrange
        close_ride = RideEntity(
            id=2,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc) + timedelta(hours=12),  # 12h no futuro
            price=100.0,
            status=RideStatus.SCHEDULED,
        )
        ride_repository.add_ride(close_ride)
        
        use_case = CancelarAgendamentoUseCase(ride_repository)
        input_data = CancelarAgendamentoInput(ride_id=2, user_id=100)
        
        # Act
        result = use_case.execute(input_data)
        
        # Assert
        assert result.ride.status == RideStatus.CANCELLED
        assert result.refund_percentage == 0.5  # 50%
        assert result.penalty_applied is True
    
    def test_cancelar_por_instrutor_deve_funcionar(self, ride_repository):
        """Instrutor também pode cancelar a aula."""
        # Arrange
        ride = RideEntity(
            id=3,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc) + timedelta(hours=48),
            price=100.0,
            status=RideStatus.SCHEDULED,
        )
        ride_repository.add_ride(ride)
        
        use_case = CancelarAgendamentoUseCase(ride_repository)
        input_data = CancelarAgendamentoInput(ride_id=3, user_id=1)  # Instrutor
        
        # Act
        result = use_case.execute(input_data)
        
        # Assert
        assert result.ride.status == RideStatus.CANCELLED
    
    def test_cancelar_por_terceiro_deve_falhar(self, ride_repository):
        """Usuário não participante não pode cancelar."""
        # Arrange
        ride = RideEntity(
            id=4,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc) + timedelta(hours=48),
            price=100.0,
            status=RideStatus.SCHEDULED,
        )
        ride_repository.add_ride(ride)
        
        use_case = CancelarAgendamentoUseCase(ride_repository)
        input_data = CancelarAgendamentoInput(ride_id=4, user_id=999)  # Terceiro
        
        # Act & Assert
        with pytest.raises(UnauthorizedRideActionException):
            use_case.execute(input_data)
    
    def test_cancelar_aula_em_andamento_deve_falhar(self, ride_repository):
        """Não pode cancelar aula que já está em andamento."""
        # Arrange
        in_progress_ride = RideEntity(
            id=5,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc),
            price=100.0,
            status=RideStatus.IN_PROGRESS,
        )
        ride_repository.add_ride(in_progress_ride)
        
        use_case = CancelarAgendamentoUseCase(ride_repository)
        input_data = CancelarAgendamentoInput(ride_id=5, user_id=100)
        
        # Act & Assert
        with pytest.raises(RideStatusTransitionException):
            use_case.execute(input_data)

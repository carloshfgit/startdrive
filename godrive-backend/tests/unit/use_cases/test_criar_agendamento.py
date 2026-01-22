"""
Testes unitários para CriarAgendamentoUseCase.
"""
import pytest
from datetime import datetime, timezone, timedelta, time

from app.application.use_cases.criar_agendamento import (
    CriarAgendamentoUseCase,
    CriarAgendamentoInput,
)
from app.domain.exceptions.ride import (
    RideScheduleInPastException,
    SlotNotAvailableException,
)
from app.domain.exceptions.instructor import InstructorNotFoundException
from app.domain.entities.ride import RideStatus


class TestCriarAgendamentoUseCase:
    """Testes para o caso de uso Criar Agendamento."""
    
    def test_criar_agendamento_sucesso(
        self, ride_repository, instructor_repository, availability_service, future_datetime
    ):
        """Deve criar agendamento com sucesso quando todos dados são válidos."""
        # Arrange
        use_case = CriarAgendamentoUseCase(
            ride_repository, instructor_repository, availability_service
        )
        
        # Ajusta horário para um slot disponível
        scheduled_at = future_datetime.replace(hour=10, minute=0, second=0, microsecond=0)
        
        input_data = CriarAgendamentoInput(
            student_id=100,
            instructor_id=1,
            scheduled_at=scheduled_at,
            pickup_latitude=-23.55,
            pickup_longitude=-46.63,
        )
        
        # Act
        result = use_case.execute(input_data)
        
        # Assert
        assert result.ride is not None
        assert result.ride.id == 1
        assert result.ride.student_id == 100
        assert result.ride.instructor_id == 1
        assert result.ride.price == 100.0  # hourly_rate do mock
        assert result.ride.status == RideStatus.PENDING
    
    def test_criar_agendamento_no_passado_deve_falhar(
        self, ride_repository, instructor_repository, availability_service, past_datetime
    ):
        """Deve lançar exceção ao agendar no passado."""
        # Arrange
        use_case = CriarAgendamentoUseCase(
            ride_repository, instructor_repository, availability_service
        )
        
        input_data = CriarAgendamentoInput(
            student_id=100,
            instructor_id=1,
            scheduled_at=past_datetime,
        )
        
        # Act & Assert
        with pytest.raises(RideScheduleInPastException):
            use_case.execute(input_data)
    
    def test_criar_agendamento_instrutor_inexistente_deve_falhar(
        self, ride_repository, instructor_repository, availability_service, future_datetime
    ):
        """Deve lançar exceção se instrutor não existir."""
        # Arrange
        use_case = CriarAgendamentoUseCase(
            ride_repository, instructor_repository, availability_service
        )
        
        scheduled_at = future_datetime.replace(hour=10, minute=0)
        
        input_data = CriarAgendamentoInput(
            student_id=100,
            instructor_id=999,  # ID inexistente
            scheduled_at=scheduled_at,
        )
        
        # Act & Assert
        with pytest.raises(InstructorNotFoundException):
            use_case.execute(input_data)
    
    def test_criar_agendamento_horario_indisponivel_deve_falhar(
        self, ride_repository, instructor_repository, future_datetime
    ):
        """Deve lançar exceção se horário não estiver disponível."""
        # Arrange
        # Mock sem slots disponíveis
        from tests.unit.use_cases.conftest import MockAvailabilityService
        empty_availability = MockAvailabilityService(available_slots=[])
        
        use_case = CriarAgendamentoUseCase(
            ride_repository, instructor_repository, empty_availability
        )
        
        scheduled_at = future_datetime.replace(hour=10, minute=0)
        
        input_data = CriarAgendamentoInput(
            student_id=100,
            instructor_id=1,
            scheduled_at=scheduled_at,
        )
        
        # Act & Assert
        with pytest.raises(SlotNotAvailableException):
            use_case.execute(input_data)

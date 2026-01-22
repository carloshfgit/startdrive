"""
Testes unitários para IniciarAulaUseCase e FinalizarAulaUseCase.
"""
import pytest
from datetime import datetime, timezone, timedelta

from app.application.use_cases.iniciar_aula import (
    IniciarAulaUseCase,
    IniciarAulaInput,
)
from app.application.use_cases.finalizar_aula import (
    FinalizarAulaUseCase,
    FinalizarAulaInput,
)
from app.domain.entities.ride import RideEntity, RideStatus
from app.domain.exceptions.ride import (
    RideNotFoundException,
    RideStatusTransitionException,
    UnauthorizedRideActionException,
    RideTooFarToStartException,
)


class TestIniciarAulaUseCase:
    """Testes para o caso de uso Iniciar Aula."""
    
    def test_iniciar_aula_sucesso(self, ride_repository):
        """Deve iniciar aula quando instrutor está próximo."""
        # Arrange
        ride = RideEntity(
            id=1,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc),
            price=100.0,
            status=RideStatus.SCHEDULED,
            pickup_latitude=-23.5505,
            pickup_longitude=-46.6333,
        )
        ride_repository.add_ride(ride)
        
        use_case = IniciarAulaUseCase(ride_repository)
        input_data = IniciarAulaInput(
            ride_id=1,
            instructor_user_id=1,
            # Localização muito próxima (mesma)
            current_latitude=-23.5505,
            current_longitude=-46.6333,
        )
        
        # Act
        result = use_case.execute(input_data)
        
        # Assert
        assert result.ride.status == RideStatus.IN_PROGRESS
    
    def test_iniciar_aula_muito_longe_deve_falhar(self, ride_repository):
        """Deve falhar se instrutor estiver longe do local."""
        # Arrange
        ride = RideEntity(
            id=2,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc),
            price=100.0,
            status=RideStatus.SCHEDULED,
            pickup_latitude=-23.5505,
            pickup_longitude=-46.6333,
        )
        ride_repository.add_ride(ride)
        
        use_case = IniciarAulaUseCase(ride_repository)
        input_data = IniciarAulaInput(
            ride_id=2,
            instructor_user_id=1,
            # Localização distante (1km+)
            current_latitude=-23.5600,
            current_longitude=-46.6500,
        )
        
        # Act & Assert
        with pytest.raises(RideTooFarToStartException):
            use_case.execute(input_data)
    
    def test_iniciar_aula_sem_local_definido_ignora_geofencing(self, ride_repository):
        """Deve iniciar mesmo longe se não tiver local definido."""
        # Arrange
        ride = RideEntity(
            id=3,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc),
            price=100.0,
            status=RideStatus.SCHEDULED,
            pickup_latitude=None,  # Sem local
            pickup_longitude=None,
        )
        ride_repository.add_ride(ride)
        
        use_case = IniciarAulaUseCase(ride_repository)
        input_data = IniciarAulaInput(
            ride_id=3,
            instructor_user_id=1,
            current_latitude=-23.5600,
            current_longitude=-46.6500,
        )
        
        # Act
        result = use_case.execute(input_data)
        
        # Assert
        assert result.ride.status == RideStatus.IN_PROGRESS
    
    def test_iniciar_aula_por_nao_instrutor_deve_falhar(self, ride_repository):
        """Apenas o instrutor responsável pode iniciar."""
        # Arrange
        ride = RideEntity(
            id=4,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc),
            price=100.0,
            status=RideStatus.SCHEDULED,
        )
        ride_repository.add_ride(ride)
        
        use_case = IniciarAulaUseCase(ride_repository)
        input_data = IniciarAulaInput(
            ride_id=4,
            instructor_user_id=999,  # Outro usuário
            current_latitude=-23.55,
            current_longitude=-46.63,
        )
        
        # Act & Assert
        with pytest.raises(UnauthorizedRideActionException):
            use_case.execute(input_data)


class TestFinalizarAulaUseCase:
    """Testes para o caso de uso Finalizar Aula."""
    
    def test_finalizar_aula_sucesso(self, ride_repository):
        """Deve finalizar aula em andamento."""
        # Arrange
        ride = RideEntity(
            id=10,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc),
            price=100.0,
            status=RideStatus.IN_PROGRESS,
        )
        ride_repository.add_ride(ride)
        
        use_case = FinalizarAulaUseCase(ride_repository)
        input_data = FinalizarAulaInput(ride_id=10, instructor_user_id=1)
        
        # Act
        result = use_case.execute(input_data)
        
        # Assert
        assert result.ride.status == RideStatus.COMPLETED
    
    def test_finalizar_aula_nao_iniciada_deve_falhar(self, ride_repository):
        """Não pode finalizar aula que não está em andamento."""
        # Arrange
        ride = RideEntity(
            id=11,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc),
            price=100.0,
            status=RideStatus.SCHEDULED,  # Não iniciada
        )
        ride_repository.add_ride(ride)
        
        use_case = FinalizarAulaUseCase(ride_repository)
        input_data = FinalizarAulaInput(ride_id=11, instructor_user_id=1)
        
        # Act & Assert
        with pytest.raises(RideStatusTransitionException):
            use_case.execute(input_data)
    
    def test_finalizar_por_nao_instrutor_deve_falhar(self, ride_repository):
        """Apenas o instrutor responsável pode finalizar."""
        # Arrange
        ride = RideEntity(
            id=12,
            student_id=100,
            instructor_id=1,
            scheduled_at=datetime.now(timezone.utc),
            price=100.0,
            status=RideStatus.IN_PROGRESS,
        )
        ride_repository.add_ride(ride)
        
        use_case = FinalizarAulaUseCase(ride_repository)
        input_data = FinalizarAulaInput(ride_id=12, instructor_user_id=100)  # Aluno
        
        # Act & Assert
        with pytest.raises(UnauthorizedRideActionException):
            use_case.execute(input_data)

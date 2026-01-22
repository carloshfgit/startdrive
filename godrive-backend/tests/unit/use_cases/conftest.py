"""
Fixtures compartilhados para testes de Use Cases.
"""
import pytest
from datetime import datetime, timezone, timedelta, time
from typing import Optional, List

from app.domain.entities.ride import RideEntity, RideStatus
from app.domain.entities.instructor import InstructorEntity


class MockRideRepository:
    """
    Mock do IRideRepository para testes unitários.
    Armazena rides em memória.
    """
    
    def __init__(self):
        self._rides: dict[int, RideEntity] = {}
        self._next_id = 1
    
    def create(self, ride: RideEntity) -> RideEntity:
        ride.id = self._next_id
        self._next_id += 1
        self._rides[ride.id] = ride
        return ride
    
    def get_by_id(self, ride_id: int) -> Optional[RideEntity]:
        return self._rides.get(ride_id)
    
    def get_by_student(self, student_id: int) -> List[RideEntity]:
        return [r for r in self._rides.values() if r.student_id == student_id]
    
    def get_by_instructor(self, instructor_id: int) -> List[RideEntity]:
        return [r for r in self._rides.values() if r.instructor_id == instructor_id]
    
    def update(self, ride: RideEntity) -> RideEntity:
        self._rides[ride.id] = ride
        return ride
    
    def add_ride(self, ride: RideEntity) -> None:
        """Helper para adicionar ride pré-existente."""
        self._rides[ride.id] = ride


class MockInstructorRepository:
    """
    Mock do IInstructorRepository para testes unitários.
    """
    
    def __init__(self, default_instructor: Optional[InstructorEntity] = None):
        self._default = default_instructor or InstructorEntity(
            id=1,
            user_id=1,
            latitude=-23.55,
            longitude=-46.63,
            hourly_rate=100.0,
            full_name="Instrutor Teste",
            status="approved"
        )
    
    def get_by_id(self, instructor_id: int) -> Optional[InstructorEntity]:
        if instructor_id == self._default.id:
            return self._default
        return None
    
    def get_by_user_id(self, user_id: int) -> Optional[InstructorEntity]:
        if user_id == self._default.user_id:
            return self._default
        return None
    
    def get_by_radius(self, lat: float, lng: float, radius_km: float) -> List[InstructorEntity]:
        return [self._default]
    
    def create(self, instructor: InstructorEntity) -> InstructorEntity:
        return instructor
    
    def update(self, instructor: InstructorEntity) -> InstructorEntity:
        return instructor


class MockAvailabilityService:
    """
    Mock do IAvailabilityService para testes unitários.
    """
    
    def __init__(self, available_slots: Optional[List[time]] = None):
        self._slots = available_slots or [
            time(8, 0), time(9, 0), time(10, 0), 
            time(11, 0), time(14, 0), time(15, 0)
        ]
    
    def get_available_slots(self, instructor_id: int, query_date) -> List[time]:
        return self._slots


@pytest.fixture
def ride_repository():
    """Fixture que retorna um MockRideRepository limpo."""
    return MockRideRepository()


@pytest.fixture
def instructor_repository():
    """Fixture que retorna um MockInstructorRepository."""
    return MockInstructorRepository()


@pytest.fixture
def availability_service():
    """Fixture que retorna um MockAvailabilityService."""
    return MockAvailabilityService()


@pytest.fixture
def future_datetime():
    """Retorna uma data no futuro para agendamentos."""
    return datetime.now(timezone.utc) + timedelta(days=2)


@pytest.fixture
def past_datetime():
    """Retorna uma data no passado (inválida para agendamento)."""
    return datetime.now(timezone.utc) - timedelta(hours=1)

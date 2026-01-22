# Adapters
# Adaptadores que envolvem repositories/services legados para implementar interfaces de domínio.

from app.infrastructure.repositories.adapters.ride_repository_adapter import RideRepositoryAdapter
from app.infrastructure.repositories.adapters.instructor_repository_adapter import InstructorRepositoryAdapter
from app.infrastructure.repositories.adapters.availability_service_adapter import AvailabilityServiceAdapter

__all__ = [
    "RideRepositoryAdapter",
    "InstructorRepositoryAdapter",
    "AvailabilityServiceAdapter",
]

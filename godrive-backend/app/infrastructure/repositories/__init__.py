# Infrastructure Repositories
# Implementações concretas dos repositories que usam SQLAlchemy.

from .user_repository import UserRepository
from .instructor_repository import InstructorRepository
from .ride_repository import RideRepository
from .availability_repository import AvailabilityRepository
from .review_repository import ReviewRepository
from .course_repository import CourseRepository
from .quiz_repository import QuizRepository

# Adapters para interfaces de domínio
from .adapters import (
    RideRepositoryAdapter,
    InstructorRepositoryAdapter,
    AvailabilityServiceAdapter,
)

__all__ = [
    # Repositories
    "UserRepository",
    "InstructorRepository",
    "RideRepository",
    "AvailabilityRepository",
    "ReviewRepository",
    "CourseRepository",
    "QuizRepository",
    # Domain adapters
    "RideRepositoryAdapter",
    "InstructorRepositoryAdapter",
    "AvailabilityServiceAdapter",
]

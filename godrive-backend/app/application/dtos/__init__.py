"""
DTOs (Data Transfer Objects) - Application Layer

Objetos puros para transferência de dados entre camadas.
Sem dependência de frameworks (Pydantic, SQLAlchemy).
"""
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional, List


# ==================== USER ====================
@dataclass
class CreateUserDTO:
    """DTO para criação de usuário."""
    full_name: str
    email: str


# ==================== RIDE ====================
@dataclass
class CreateRideDTO:
    """DTO para criação de agendamento."""
    instructor_id: int
    scheduled_at: datetime
    pickup_latitude: float
    pickup_longitude: float


# ==================== INSTRUCTOR ====================
@dataclass
class CreateInstructorDTO:
    """DTO para criação de perfil de instrutor."""
    bio: str
    hourly_rate: float
    cnh_category: str
    vehicle_model: str
    latitude: float
    longitude: float


# ==================== AVAILABILITY ====================
@dataclass
class CreateAvailabilityDTO:
    """DTO para criação de disponibilidade."""
    day_of_week: int  # 0=Segunda, 6=Domingo
    start_time: time
    end_time: time


# ==================== REVIEW ====================
@dataclass
class CreateReviewDTO:
    """DTO para criação de avaliação."""
    ride_id: int
    rating: int
    comment: Optional[str] = None


# ==================== COURSE ====================
@dataclass
class CreateLessonDTO:
    """DTO para criação de aula."""
    title: str
    video_url: Optional[str] = None
    duration_seconds: int = 0
    description: Optional[str] = None
    order: int = 0


@dataclass
class CreateModuleDTO:
    """DTO para criação de módulo."""
    title: str
    order: int = 0
    lessons: List[CreateLessonDTO] = None

    def __post_init__(self):
        if self.lessons is None:
            self.lessons = []


@dataclass
class CreateCourseDTO:
    """DTO para criação de curso."""
    title: str
    description: Optional[str] = None
    price: float = 0.0
    cover_image_url: Optional[str] = None
    is_published: bool = False


# ==================== QUIZ ====================
@dataclass
class CreateOptionDTO:
    """DTO para criação de opção de questão."""
    text: str
    is_correct: bool = False


@dataclass
class CreateQuestionDTO:
    """DTO para criação de questão."""
    text: str
    points: int = 1
    order: int = 0
    options: List[CreateOptionDTO] = None

    def __post_init__(self):
        if self.options is None:
            self.options = []


@dataclass
class CreateQuizDTO:
    """DTO para criação de quiz."""
    title: str
    module_id: Optional[int] = None
    description: Optional[str] = None
    passing_score: float = 70.0

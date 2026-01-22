from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- AULAS (LESSONS) ---

class LessonCreate(BaseModel):
    title: str
    video_url: Optional[str] = None
    duration_seconds: int = 0
    description: Optional[str] = None
    order: int = 0

class LessonResponse(BaseModel):
    id: int
    module_id: int
    title: str
    video_url: Optional[str] = None
    duration_seconds: int
    description: Optional[str] = None
    order: int

    class Config:
        from_attributes = True

# --- MÓDULOS (MODULES) ---

class ModuleCreate(BaseModel):
    title: str
    order: int = 0
    # Opcional: permitir criar aulas já dentro do módulo de uma vez
    lessons: List[LessonCreate] = [] 

class ModuleResponse(BaseModel):
    id: int
    course_id: int
    title: str
    order: int
    # Retorna as aulas aninhadas para facilitar o frontend
    lessons: List[LessonResponse] = []

    class Config:
        from_attributes = True

# --- CURSOS (COURSES) ---

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = 0.0
    cover_image_url: Optional[str] = None
    is_published: bool = False

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    cover_image_url: Optional[str] = None
    is_published: bool
    created_at: datetime
    
    # Lista de módulos (que contém lista de aulas)
    # Isso permite renderizar a página do curso com uma única chamada
    modules: List[ModuleResponse] = []

    class Config:
        from_attributes = True

# --- MATRÍCULAS (ENROLLMENTS) ---

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    purchased_at: datetime
    price_paid: float
    
    # Podemos incluir dados do curso resumidos aqui se necessário
    course: Optional[CourseResponse] = None 

    class Config:
        from_attributes = True
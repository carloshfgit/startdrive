from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse, ModuleCreate, LessonCreate, EnrollmentResponse
from app.repositories.course_repository import CourseRepository

router = APIRouter()
course_repo = CourseRepository()

@router.get("/", response_model=List[CourseResponse])
def list_courses(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Lista todos os cursos publicados disponíveis na plataforma.
    """
    return course_repo.get_all(db, skip=skip, limit=limit, published_only=True)

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser) # Apenas Admin pode criar
):
    """
    Cria um novo curso (Área Administrativa).
    """
    return course_repo.create(db, course=course_in)

@router.get("/{course_id}", response_model=CourseResponse)
def get_course_details(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retorna a grade curricular do curso.
    **Regra de Negócio:** Se o aluno NÃO estiver matriculado, o campo `video_url` das aulas será removido (None).
    """
    course = course_repo.get_by_id(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    
    # Verifica se o usuário comprou o curso
    enrollment = course_repo.get_enrollment(db, user_id=current_user.id, course_id=course.id)
    
    # Lógica de Proteção de Conteúdo (DRM light)
    # Se não for Admin E não estiver matriculado: esconde os links dos vídeos
    if not current_user.is_superuser and not enrollment:
        for module in course.modules:
            for lesson in module.lessons:
                lesson.video_url = None # Mascara o link
                
    return course

@router.post("/{course_id}/enroll", response_model=EnrollmentResponse)
def enroll_student(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Realiza a matrícula do aluno no curso.
    
    TODO: Futuramente, este endpoint será chamado pelo Webhook do Stripe após pagamento confirmado.
    Por enquanto, permite matrícula direta (Cursos Gratuitos ou Teste).
    """
    course = course_repo.get_by_id(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    
    if course_repo.get_enrollment(db, user_id=current_user.id, course_id=course_id):
        raise HTTPException(status_code=400, detail="Você já está matriculado neste curso.")
    
    # Registra matrícula
    return course_repo.enroll_user(db, user_id=current_user.id, course_id=course_id, price_paid=course.price)

# --- Sub-recursos (Adicionar Conteúdo) ---

@router.post("/{course_id}/modules", response_model=CourseResponse)
def add_module(
    course_id: int,
    module_in: ModuleCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """Adiciona um módulo ao curso."""
    course = course_repo.get_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
        
    course_repo.create_module(db, course_id, module_in)
    db.refresh(course) # Recarrega para retornar a estrutura atualizada
    return course

@router.post("/{course_id}/modules/{module_id}/lessons", response_model=CourseResponse)
def add_lesson(
    course_id: int,
    module_id: int,
    lesson_in: LessonCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """Adiciona uma aula a um módulo existente."""
    # (Poderíamos adicionar validação se o módulo pertence ao curso aqui)
    course_repo.create_lesson(db, module_id, lesson_in)
    
    course = course_repo.get_by_id(db, course_id)
    return course
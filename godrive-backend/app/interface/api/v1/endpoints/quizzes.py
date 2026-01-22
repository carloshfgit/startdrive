# app/api/v1/endpoints/quizzes.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.interface.api import deps
from app.infrastructure.db.models.user import User
from app.interface.api.schemas.quiz import (
    QuizCreate, QuizAdmin, QuizPublic, 
    QuestionCreate, QuizSubmission, QuizResultResponse
)
from app.infrastructure.repositories.quiz_repository import QuizRepository
from app.application.use_cases.quiz.quiz_service import QuizService
from app.application.dtos import CreateQuizDTO, CreateQuestionDTO, CreateOptionDTO

router = APIRouter()
repo = QuizRepository()
service = QuizService()

# --- ÁREA DO ADMIN (Criação) ---

@router.post("/", response_model=QuizAdmin, status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz_in: QuizCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """Admin: Cria um novo simulado (cabeçalho)."""
    # Converte Pydantic Schema para DTO (Clean Architecture)
    quiz_dto = CreateQuizDTO(
        title=quiz_in.title,
        module_id=quiz_in.module_id,
        description=quiz_in.description,
        passing_score=quiz_in.passing_score,
    )
    return repo.create_quiz(db, quiz_dto)

@router.post("/{quiz_id}/questions", response_model=QuizAdmin)
def add_question_to_quiz(
    quiz_id: int,
    question_in: QuestionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """Admin: Adiciona uma pergunta (com opções) ao simulado."""
    quiz = repo.get_quiz_full(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Simulado não encontrado")
    
    # Converte Pydantic Schema para DTO (Clean Architecture)
    options_dto = [CreateOptionDTO(text=opt.text, is_correct=opt.is_correct) for opt in question_in.options]
    question_dto = CreateQuestionDTO(
        text=question_in.text,
        points=question_in.points,
        order=question_in.order,
        options=options_dto,
    )
    repo.add_question(db, quiz_id, question_dto)
    
    # Recarrega para retornar estrutura atualizada
    return repo.get_quiz_full(db, quiz_id)


# --- ÁREA DO ALUNO (Consumo) ---

@router.get("/{quiz_id}", response_model=QuizPublic)
def get_quiz_details(
    quiz_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Aluno: Abre o simulado para responder.
    IMPORTANTE: O schema 'QuizPublic' remove automaticamente o campo 'is_correct'.
    """
    quiz = repo.get_quiz_full(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Simulado não encontrado")
    return quiz

@router.post("/{quiz_id}/submit", response_model=QuizResultResponse)
def submit_quiz_answers(
    quiz_id: int,
    submission: QuizSubmission,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Aluno: Envia as respostas. O servidor corrige e devolve a nota na hora.
    """
    return service.submit_quiz(db, current_user.id, quiz_id, submission)
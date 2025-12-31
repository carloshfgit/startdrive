# app/schemas/quiz.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- OPÇÕES (OPTIONS) ---

class OptionBase(BaseModel):
    text: str

class OptionCreate(OptionBase):
    is_correct: bool = False

class OptionAdmin(OptionBase):
    id: int
    is_correct: bool
    
    class Config:
        from_attributes = True

class OptionPublic(OptionBase):
    """Visualização do Aluno: NÃO revela se é a correta."""
    id: int
    
    class Config:
        from_attributes = True

# --- QUESTÕES (QUESTIONS) ---

class QuestionBase(BaseModel):
    text: str
    points: int = 1
    order: int = 0

class QuestionCreate(QuestionBase):
    # Permite criar opções aninhadas na criação da pergunta
    options: List[OptionCreate]

class QuestionAdmin(QuestionBase):
    id: int
    options: List[OptionAdmin] = []
    
    class Config:
        from_attributes = True

class QuestionPublic(QuestionBase):
    id: int
    options: List[OptionPublic] = []
    
    class Config:
        from_attributes = True

# --- QUIZ (SIMULADO) ---

class QuizCreate(BaseModel):
    module_id: Optional[int] = None # Se None, é um quiz solto
    title: str
    description: Optional[str] = None
    passing_score: float = 70.0

class QuizAdmin(BaseModel):
    id: int
    module_id: int
    title: str
    description: Optional[str] = None
    passing_score: float
    
    # Admin vê tudo
    questions: List[QuestionAdmin] = []
    
    class Config:
        from_attributes = True

class QuizPublic(BaseModel):
    """
    O que o aluno vê ao abrir o simulado.
    """
    id: int
    title: str
    description: Optional[str] = None
    passing_score: float
    questions: List[QuestionPublic] = []
    
    class Config:
        from_attributes = True

# --- SUBMISSÃO E RESULTADOS ---

class AnswerItem(BaseModel):
    question_id: int
    selected_option_id: int

class QuizSubmission(BaseModel):
    answers: List[AnswerItem]

class QuizResultResponse(BaseModel):
    """
    Retorno imediato após o submit.
    """
    attempt_id: int
    score_achieved: float
    passed: bool
    correct_count: int
    total_questions: int
# app/models/quiz.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.id"), nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    passing_score = Column(Float, default=70.0) # Nota mínima para passar (ex: 70%)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    module = relationship("Module", backref="quizzes")
    questions = relationship("Question", backref="quiz", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    
    text = Column(Text, nullable=False) # Enunciado
    order = Column(Integer, default=0)
    points = Column(Integer, default=1) # Peso da questão

    # Relacionamentos
    options = relationship("QuestionOption", backref="question", cascade="all, delete-orphan")


class QuestionOption(Base):
    __tablename__ = "quiz_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False) # Define se é a resposta certa


class UserQuizAttempt(Base):
    """
    Registra a tentativa de um aluno ao realizar um simulado.
    """
    __tablename__ = "user_quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    
    score_achieved = Column(Float, nullable=False) # Nota final (0 a 100)
    passed = Column(Boolean, default=False)        # Se atingiu o passing_score
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User", backref="quiz_attempts")
    quiz = relationship("Quiz", backref="attempts")
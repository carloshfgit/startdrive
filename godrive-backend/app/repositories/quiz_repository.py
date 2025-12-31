# app/repositories/quiz_repository.py
from sqlalchemy.orm import Session, joinedload
from app.models.quiz import Quiz, Question, QuestionOption, UserQuizAttempt
from app.schemas.quiz import QuizCreate, QuestionCreate

class QuizRepository:
    
    def create_quiz(self, db: Session, quiz_in: QuizCreate):
        db_quiz = Quiz(
            module_id=quiz_in.module_id,
            title=quiz_in.title,
            description=quiz_in.description,
            passing_score=quiz_in.passing_score
        )
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        return db_quiz

    def add_question(self, db: Session, quiz_id: int, question_in: QuestionCreate):
        # 1. Cria a pergunta
        db_question = Question(
            quiz_id=quiz_id,
            text=question_in.text,
            points=question_in.points,
            order=question_in.order
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        # 2. Cria as opções associadas
        for opt in question_in.options:
            db_option = QuestionOption(
                question_id=db_question.id,
                text=opt.text,
                is_correct=opt.is_correct
            )
            db.add(db_option)
        
        db.commit()
        db.refresh(db_question) # Recarrega com as opções
        return db_question

    def get_quiz_full(self, db: Session, quiz_id: int):
        """
        Busca o quiz carregando todas as perguntas e opções (Eager Loading).
        Essencial para performance, evita o problema N+1.
        """
        return db.query(Quiz)\
                 .options(
                     joinedload(Quiz.questions).joinedload(Question.options)
                 )\
                 .filter(Quiz.id == quiz_id)\
                 .first()

    def get_question_by_id(self, db: Session, question_id: int):
        """Útil para validar respostas individualmente."""
        return db.query(Question).filter(Question.id == question_id).first()
        
    def get_option_by_id(self, db: Session, option_id: int):
        return db.query(QuestionOption).filter(QuestionOption.id == option_id).first()

    def create_attempt(self, db: Session, user_id: int, quiz_id: int, score: float, passed: bool):
        db_attempt = UserQuizAttempt(
            user_id=user_id,
            quiz_id=quiz_id,
            score_achieved=score,
            passed=passed
        )
        db.add(db_attempt)
        db.commit()
        db.refresh(db_attempt)
        return db_attempt
# app/services/quiz_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.infrastructure.repositories.quiz_repository import QuizRepository
from app.interface.api.schemas.quiz import QuizSubmission, QuizResultResponse

class QuizService:
    def __init__(self):
        self.repo = QuizRepository()

    def submit_quiz(self, db: Session, user_id: int, quiz_id: int, submission: QuizSubmission) -> QuizResultResponse:
        """
        Corrige o simulado, calcula a nota e salva o histórico.
        """
        # 1. Busca o quiz completo (com o gabarito) do banco
        quiz = self.repo.get_quiz_full(db, quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Simulado não encontrado.")

        # 2. Cria um mapa para acesso rápido às respostas corretas
        # Estrutura: { question_id: correct_option_id }
        correct_answers_map = {}
        for question in quiz.questions:
            for option in question.options:
                if option.is_correct:
                    correct_answers_map[question.id] = option.id
                    break # Assume apenas 1 correta por questão por enquanto

        # 3. Correção
        correct_count = 0
        total_questions = len(quiz.questions)
        
        # Se o quiz não tiver perguntas, evita divisão por zero
        if total_questions == 0:
            return QuizResultResponse(
                attempt_id=0, score_achieved=0, passed=False, 
                correct_count=0, total_questions=0
            )

        for answer in submission.answers:
            # Verifica se a questão existe no gabarito
            if answer.question_id in correct_answers_map:
                # Compara a opção enviada pelo aluno com a correta
                if answer.selected_option_id == correct_answers_map[answer.question_id]:
                    correct_count += 1

        # 4. Cálculo da Nota (0 a 100)
        score = (correct_count / total_questions) * 100
        passed = score >= quiz.passing_score

        # 5. Persistência (Salvar a tentativa)
        attempt = self.repo.create_attempt(
            db=db,
            user_id=user_id,
            quiz_id=quiz.id,
            score=score,
            passed=passed
        )

        return QuizResultResponse(
            attempt_id=attempt.id,
            score_achieved=round(score, 1),
            passed=passed,
            correct_count=correct_count,
            total_questions=total_questions
        )
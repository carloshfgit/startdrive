# app/api/v1/endpoints/payments.py
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.interface.api import deps
from app.infrastructure.db.models.user import User
from app.infrastructure.db.models.ride import Ride, RideStatus
from app.infrastructure.db.models.course import Course # <--- Novo Import
from app.application.use_cases.payment.payment_service import PaymentService
from app.infrastructure.repositories.course_repository import CourseRepository # <--- Novo Import

router = APIRouter()
payment_service = PaymentService()
course_repo = CourseRepository() # <--- Instância

# --- PAGAMENTO DE AULAS (RIDE) ---

@router.post("/create-intent/ride/{ride_id}")
def create_ride_payment_intent(
    ride_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Inicia o pagamento de uma aula (Booking)."""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")
    
    if ride.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não é o aluno desta aula.")
    
    if ride.status != RideStatus.PENDING_PAYMENT:
        raise HTTPException(status_code=400, detail="Esta aula não está pendente de pagamento.")

    instructor_stripe_id = ride.instructor.stripe_account_id
    if not instructor_stripe_id:
        raise HTTPException(
            status_code=400, 
            detail="O instrutor não possui conta bancária configurada."
        )

    try:
        # Chama o método específico para Rides (renomeado no service)
        return payment_service.create_ride_payment_intent(
            ride_id=ride.id,
            amount=ride.price,
            instructor_stripe_id=instructor_stripe_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- PAGAMENTO DE CURSOS (NOVO) ---

@router.post("/create-intent/course/{course_id}")
def create_course_payment_intent(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Inicia o pagamento de um curso (LMS)."""
    course = course_repo.get_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    
    # Verifica se já comprou
    if course_repo.get_enrollment(db, current_user.id, course_id):
        raise HTTPException(status_code=400, detail="Você já possui este curso.")

    try:
        return payment_service.create_course_payment_intent(
            course_id=course.id,
            amount=course.price,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- WEBHOOK (O CÉREBRO) ---

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(deps.get_db)):
    body = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = payment_service.process_webhook_event(body, sig_header)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        metadata = payment_intent.get("metadata", {})
        product_type = metadata.get("product_type")

        # ROTA 1: Pagamento de AULA
        if product_type == "ride":
            ride_id = int(metadata.get("ride_id"))
            ride = db.query(Ride).filter(Ride.id == ride_id).first()
            if ride:
                ride.status = RideStatus.SCHEDULED
                db.commit()
                print(f"WEBHOOK: Aula {ride_id} confirmada.")

        # ROTA 2: Pagamento de CURSO
        elif product_type == "course":
            course_id = int(metadata.get("course_id"))
            user_id = int(metadata.get("user_id"))
            
            # Busca o preço real pago (convertendo centavos de volta)
            amount_paid = payment_intent["amount"] / 100.0
            
            # Efetiva a matrícula
            # Verifica novamente se já não existe para evitar erro de constraint
            if not course_repo.get_enrollment(db, user_id, course_id):
                course_repo.enroll_user(db, user_id, course_id, amount_paid)
                print(f"WEBHOOK: Matrícula confirmada User {user_id} -> Curso {course_id}")

    return {"status": "success"}
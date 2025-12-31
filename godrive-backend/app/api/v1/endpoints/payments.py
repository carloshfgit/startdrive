# app/api/v1/endpoints/payments.py
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.ride import Ride, RideStatus
from app.services.payment_service import PaymentService

router = APIRouter()
payment_service = PaymentService()

@router.post("/create-intent/{ride_id}")
def create_payment_intent(
    ride_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Inicia o pagamento de uma aula.
    Retorna o 'client_secret' para o App Mobile processar o cartão.
    """
    # 1. Buscar a aula
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")
    
    # 2. Validações
    if ride.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não é o aluno desta aula.")
    
    if ride.status != RideStatus.PENDING_PAYMENT:
        raise HTTPException(status_code=400, detail="Esta aula não está pendente de pagamento.")

    # 3. Obter ID Stripe do Instrutor
    instructor_stripe_id = ride.instructor.stripe_account_id
    
    # [CORREÇÃO] Bloqueio Rígido: Não permitir pagamento sem destino configurado
    if not instructor_stripe_id:
        raise HTTPException(
            status_code=400, 
            detail="O instrutor ainda não configurou os dados bancários para recebimento."
        )

    # 4. Chamar o serviço
    try:
        result = payment_service.create_payment_intent(
            ride_id=ride.id,
            amount=ride.price,
            instructor_stripe_id=instructor_stripe_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(deps.get_db)):
    """
    Rota que o Stripe chama automaticamente quando o pagamento muda de status.
    """
    body = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = payment_service.process_webhook_event(body, sig_header)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Processar o evento
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        ride_id = int(payment_intent["metadata"]["ride_id"])
        
        # Atualizar status da aula para SCHEDULED (Confirmada)
        ride = db.query(Ride).filter(Ride.id == ride_id).first()
        if ride:
            ride.status = RideStatus.SCHEDULED
            db.commit()
            print(f"Pagamento confirmado para a aula {ride_id}")

    return {"status": "success"}
# app/services/payment_service.py
import stripe
from app.core.config import settings

if settings.STRIPE_API_KEY:
    stripe.api_key = settings.STRIPE_API_KEY

class PaymentService:
    
    def _calculate_cents(self, amount: float) -> int:
        return int(amount * 100)

    def create_ride_payment_intent(self, ride_id: int, amount: float, instructor_stripe_id: str):
        """
        Pagamento de AULA (Com Split para o Instrutor).
        """
        try:
            amount_cents = self._calculate_cents(amount)
            fee_cents = int(amount_cents * settings.PLATFORM_FEE_PERCENT)
            
            intent_data = {
                "amount": amount_cents,
                "currency": "brl",
                "automatic_payment_methods": {"enabled": True},
                "metadata": {
                    "product_type": "ride", # Identificador do tipo
                    "ride_id": str(ride_id)
                },
            }

            # Configura o Split (Instrutor recebe, Plataforma fica com a taxa)
            if instructor_stripe_id:
                intent_data["application_fee_amount"] = fee_cents
                intent_data["transfer_data"] = {
                    "destination": instructor_stripe_id,
                }
            
            intent = stripe.PaymentIntent.create(**intent_data)
            return {"client_secret": intent.client_secret, "id": intent.id}

        except stripe.error.StripeError as e:
            raise ValueError(f"Erro no Stripe: {e.user_message or str(e)}")
            
    def create_course_payment_intent(self, course_id: int, amount: float, user_id: int):
        """
        Pagamento de CURSO (Sem Split - Venda direta da Plataforma).
        """
        try:
            amount_cents = self._calculate_cents(amount)
            
            intent_data = {
                "amount": amount_cents,
                "currency": "brl",
                "automatic_payment_methods": {"enabled": True},
                "metadata": {
                    "product_type": "course", # Identificador do tipo
                    "course_id": str(course_id),
                    "user_id": str(user_id) # Precisamos saber quem matriculou
                },
            }
            
            # Sem transfer_data, o dinheiro fica todo na conta da plataforma
            intent = stripe.PaymentIntent.create(**intent_data)
            return {"client_secret": intent.client_secret, "id": intent.id}

        except stripe.error.StripeError as e:
            raise ValueError(f"Erro no Stripe: {e.user_message or str(e)}")

    def process_webhook_event(self, body: bytes, sig_header: str):
        try:
            event = stripe.Webhook.construct_event(
                payload=body,
                sig_header=sig_header,
                secret=settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError:
            raise ValueError("Payload inválido")
        except stripe.error.SignatureVerificationError:
            raise ValueError("Assinatura do Webhook inválida")
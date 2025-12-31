# app/services/payment_service.py
import stripe
from app.core.config import settings

# Configura a chave assim que o módulo é importado
if settings.STRIPE_API_KEY:
    stripe.api_key = settings.STRIPE_API_KEY

class PaymentService:
    def create_payment_intent(self, ride_id: int, amount: float, instructor_stripe_id: str):
        """
        Gera a intenção de pagamento no Stripe com Split automático.
        """
        try:
            # 1. Converter valor para centavos (Stripe usa inteiros)
            # Ex: R$ 100.00 -> 10000 centavos
            amount_cents = int(amount * 100)
            
            # 2. Calcular a comissão da plataforma
            # Ex: 15% de 10000 -> 1500 centavos
            fee_cents = int(amount_cents * settings.PLATFORM_FEE_PERCENT)
            
            # 3. Criar a Intent
            # Se o instrutor tiver conta conectada, fazemos o split via 'transfer_data'
            intent_data = {
                "amount": amount_cents,
                "currency": "brl",
                "automatic_payment_methods": {"enabled": True},
                "metadata": {"ride_id": str(ride_id)}, # ID para rastrearmos depois no Webhook
            }

            # Se o instrutor tem conta no Stripe, configuramos o Split
            if instructor_stripe_id:
                intent_data["application_fee_amount"] = fee_cents
                intent_data["transfer_data"] = {
                    "destination": instructor_stripe_id,
                }
            
            # Criação efetiva no Stripe
            intent = stripe.PaymentIntent.create(**intent_data)
            
            return {
                "client_secret": intent.client_secret, # O App usa isso para finalizar o pgto
                "id": intent.id
            }

        except stripe.error.StripeError as e:
            # Erro específico do Stripe (ex: cartão recusado, conta inválida)
            raise ValueError(f"Erro no Stripe: {e.user_message or str(e)}")
        except Exception as e:
            raise ValueError(f"Erro interno de pagamento: {str(e)}")

    def process_webhook_event(self, body: bytes, sig_header: str):
        """
        Valida a assinatura do Webhook para garantir que veio do Stripe.
        """
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
# app/services/payment_service.py
import stripe
from app.core.config import settings

# Configura a chave assim que o módulo é carregado
stripe.api_key = settings.STRIPE_API_KEY

class PaymentService:
    def create_payment_intent(self, ride_id: int, amount: float, instructor_account_id: str):
        """
        Cria uma intenção de pagamento no Stripe.
        
        Args:
            ride_id: ID da aula (para metadados)
            amount: Valor total em Reais (será convertido para centavos)
            instructor_account_id: ID da conta Stripe Connect do instrutor (para o split)
        """
        try:
            # O Stripe trabalha com centavos (R$ 50,00 -> 5000)
            amount_cents = int(amount * 100)
            
            # Cálculo do Split (Quanto fica para a plataforma?)
            fee = int(amount_cents * settings.PLATFORM_FEE_PERCENT)
            
            # Cria a Intent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='brl',
                automatic_payment_methods={'enabled': True},
                application_fee_amount=fee, # Nossa comissão
                transfer_data={
                    'destination': instructor_account_id, # O resto vai pro instrutor
                },
                metadata={'ride_id': ride_id} # Importante para o Webhook saber qual aula atualizar
            )
            
            return {
                "client_secret": intent.client_secret, # O App Mobile usa isso para abrir o checkout
                "id": intent.id
            }
            
        except Exception as e:
            # Em produção, logar o erro corretamente
            print(f"Erro no Stripe: {e}")
            raise e

    def process_webhook(self, body: bytes, sig_header: str):
        """
        Valida e processa eventos enviados pelo Stripe (ex: pagamento aprovado).
        """
        event = None
        try:
            event = stripe.Webhook.construct_event(
                body, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            raise Exception("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            raise Exception("Invalid signature")

        return event
import stripe
from app.core.config import settings

# Ініціалізація Stripe API
stripe.api_key = getattr(settings, "STRIPE_API_KEY", None)

class StripeService:
    """
    Сервіс для створення платіжних сесій Stripe.
    """
    
    @staticmethod
    async def create_checkout_session(amount: int, currency: str, order_id: int):
        """
        Створює посилання на оплату (Checkout Session).
        Сума (amount) передається в найменших одиницях (наприклад, центах).
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {'name': f'Замовлення #{order_id}'},
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{settings.SITE_URL}/success",
                cancel_url=f"{settings.SITE_URL}/cancel",
                metadata={'order_id': order_id}
            )
            return session.url
        except Exception as e:
            # Тут можна додати логування помилки
            return None

    @staticmethod
    def construct_webhook_event(payload, sig_header):
        """
        Валідація webhook від Stripe для підтвердження оплати.
        """
        try:
            return stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return None
import base64

from decouple import config
from django.utils import timezone

from cart.models import Cart, Order
from common.mailer.MailJetClient import MailJetClient


def make_carts_abandoned():
    """
    This function is used to make carts that are older than 2 days abandoned
    """
    # get carts older than 2 days
    carts = Cart.objects.filter(
        status=Cart.CartStatus.ACTIVE,
        created_at__lte=timezone.now(),
    ).update(status=Cart.CartStatus.ABANDONED)


def send_email_to_orders_older_than_5_min():
    email_client = MailJetClient()
    base_url = config("BASE_URL")
    # get carts older than 5 minutes
    orders = Order.objects.filter(
        created_at__lte=timezone.now() - timezone.timedelta(minutes=5),
        shipping_details__email__isnull=False,
        mail_is_sent=False,
    )

    for order in orders:
        result = email_client.send_mail(
            "Потврда за нарачка",
            f"Ви благодариме за нарачката! Вашата нарачка е успешно примена. Во прилог Ви ја испраќаме фактурата за нарачката.",
            order.shipping_details.email,
            attachment=base64.b64encode(
                order.generate_invoice_pdf(base_url=base_url, show_details=False)
            ).decode("utf-8"),
        )
        print(result)
        order.mail_is_sent = True
        order.save()

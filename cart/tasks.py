import base64
import logging

from celery import shared_task
from django.db import transaction

from common.mailer.MailJetClient import MailJetClient

# Configure a logger for the task
logger = logging.getLogger(__name__)


@shared_task
def generate_invoice_and_send_email_to_order(order_id):
    from .models import Order

    order = (
        Order.objects.filter(id=order_id)
        .prefetch_related(
            "order_items",
            "order_items__product",
            "order_items__attribute",
            "order_items__stock_item",
        )
        .select_related("shipping_details")
        .first()
    )

    if not order:
        logger.error(
            "No order has been found for celery to process with ID: %s", order_id
        )
        return
    pdf_file_path = order.generate_invoice_pdf(show_details=False, as_file=True)

    if order.shipping_details and order.shipping_details.email:
        try:
            with open(pdf_file_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

            email_client = MailJetClient()
            result = email_client.send_mail(
                "Потврда за нарачка",
                "Ви благодариме за нарачката! Вашата нарачка е успешно примена. Во прилог Ви ја испраќаме фактурата за нарачката.",
                order.shipping_details.email,
                attachment=encoded_pdf,
            )

            print(result)

            with transaction.atomic():
                order.mail_is_sent = True
                order.save()
            logger.info("Email sent successfully for order ID: %s", order_id)
        except Exception as e:
            logger.error("Failed to process order ID %s: %s", order_id, e)


@shared_task()
def calculate_revenue_and_profit_for_client(client_id):
    from shop.models import ShopClient
    from .models import Order

    client = ShopClient.objects.get(id=client_id)

    orders = Order.objects.filter(user=client)
    total_revenue = 0
    total_profit = 0

    for order in orders:
        total_revenue += order.total_price
        total_profit += order.profit

    client.total_revenue = total_revenue
    client.total_profit = total_profit

    client.save()

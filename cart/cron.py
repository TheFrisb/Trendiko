from django.utils import timezone

from cart.models import Cart


def make_carts_abandoned():
    """
    This function is used to make carts that are older than 2 days abandoned
    """
    # get carts older than 2 days
    carts = Cart.objects.filter(
        status=Cart.CartStatus.ACTIVE,
        created_at__lte=timezone.now(),
    ).update(status=Cart.CartStatus.ABANDONED)


# def send_email_to_orders_older_than_5_min():
#     email_client = MailJetClient()
#     orders = Order.objects.filter(
#         created_at__lte=timezone.now() - timezone.timedelta(minutes=5),
#         shipping_details__email__isnull=False,
#         mail_is_sent=False,
#     )
#
#     for order in orders:
#         pdf_file_path = order.generate_invoice_pdf(show_details=False, as_file=True)
#         with open(pdf_file_path, "rb") as pdf_file:
#             pdf_bytes = pdf_file.read()
#             encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
#
#         result = email_client.send_mail(
#             "Потврда за нарачка",
#             "Ви благодариме за нарачката! Вашата нарачка е успешно примена. Во прилог Ви ја испраќаме фактурата за нарачката.",
#             order.shipping_details.email,
#             attachment=encoded_pdf,
#         )
#         print(result)
#         order.mail_is_sent = True
#         order.save()

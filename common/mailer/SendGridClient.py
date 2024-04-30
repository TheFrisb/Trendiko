import base64

from decouple import config
from sendgrid import SendGridAPIClient, Mail
from sendgrid.helpers.mail import (
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)


class SendGridClient:
    def __init__(self):
        self.apiKey = config("SENDGRID_API_KEY")
        self.client = SendGridAPIClient(self.apiKey)

    def send_mail(self, to_email, subject, html_content, attachment=None):
        message = Mail(
            from_email="hello@trendiko.mk",
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )

        if attachment:
            attachment = Attachment(
                file_content=FileContent(base64.b64encode(attachment).decode("utf-8")),
                file_type=FileType("application/pdf"),
                file_name=FileName("price_change.pdf"),
                disposition=Disposition("attachment"),
            )
            message.attachment = attachment

        try:
            response = self.client.send(message)
            print(f"Status Code: {response.status_code}")
            print(f"Body: {response.body}")
            print(f"Headers: {response.headers}")
        except Exception as e:
            print(e.message)

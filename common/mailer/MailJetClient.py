from decouple import config
from mailjet_rest import Client


class MailJetClient:
    def __init__(self):
        self.apiKey = config("MAILJET_API_KEY")
        self.secretKey = config("MAILJET_SECRET_KEY")
        self.client = Client(auth=(self.apiKey, self.secretKey), version="v3.1")

    def send_mail(self, subject, text_part, recipient, attachment=None):
        data = {
            "Messages": [
                {
                    "From": {"Email": "info@trendiko.mk"},
                    "To": [{"Email": recipient}],
                    "Subject": subject,
                    "TextPart": text_part,
                    "Attachments": [
                        {
                            "ContentType": "application/pdf",
                            "Filename": "invoice.pdf",
                            "Base64Content": attachment,
                        }
                    ],
                }
            ]
        }

        result = self.client.send.create(data=data)
        return result.status_code

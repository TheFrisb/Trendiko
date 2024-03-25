from decouple import config
from mailjet_rest import Client


class MailJetClient:
    def __init__(self):
        self.apiKey = config("MAILJET_API_KEY")
        self.secretKey = config("MAILJET_SECRET_KEY")
        self.client = Client(auth=(self.apiKey, self.secretKey), version="v3.1")

    def send_mail(self, subject, text_part, recipients):
        data = {
            "Messages": [
                {
                    "From": {"Email": "info@trendiko.mk", "Name": "Zhivko"},
                    "To": recipients,
                    "Subject": subject,
                    "TextPart": text_part,
                    "CustomID": "AppGettingStartedTest",
                }
            ]
        }

        result = self.client.send.create(data=data)
        print(result.status_code)
        return result.status_code

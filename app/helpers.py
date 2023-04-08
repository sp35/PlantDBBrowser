from azure.communication.email import EmailClient
from django.conf import settings
from .models import Maintainer


def send_email(subject, html):
    connection_string = settings.EMAIL_CONNECTION_STRING
    sender_address = settings.EMAIL_SENDER_ADDRESS
    recipients = [
        {"address": email} for email in Maintainer.objects.values_list("email", flat=True)
    ]

    message = {
        "senderAddress": sender_address,
        "recipients": {
            "cc": recipients
        },
        "content": {
            "subject": subject,
            "html": html,
        }
    }

    try:
        client = EmailClient.from_connection_string(connection_string)
        client.begin_send(message)

    except Exception as ex:
        print(ex)

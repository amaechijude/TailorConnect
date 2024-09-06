from django.core.mail import send_mail
from django.conf import settings


def RequestEmailToDesigner(subject:str, message, SenderEmail:str, DesignerEmail:str) -> bool:
    body = f"""
    A new Request from {SenderEmail}

    {message}

    """
    try:
        send_mail(
            subject,
            body,
            SenderEmail,
            [DesignerEmail, SenderEmail],
            fail_silently=False
        )
    except ConnectionError:
        return False
    return True
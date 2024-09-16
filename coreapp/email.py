from django.core.mail import send_mail
from django.conf import settings
from .models import User


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

###### email verification for designers ########
def DesignerVerifyEmail(demail) -> bool:
    subject = f"Designer Verification Request"
    body = f"""
    A new user with email {demail} is requesting to be verified as a designer.

    Check his profile and do the needful
    """
    try:
        send_mail(
            subject,
            body,
            demail,
            [email for email in User.email.filter(is_staff=True, is_superuser=True)],
            fail_silently=False
        )
    except ConnectionError:
        return False

    return True
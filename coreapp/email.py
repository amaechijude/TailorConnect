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


##### design Request #######
def DesignRequestEmail(userEmail,brandName, brandEmail):
    subject = "Request Received"
    body = f"""do not reply this mail
    
    Hello {userEmail};
    Your request for creating a designer profile with the following detaial is recieved.
    Brand Name:-> {brandName}.
    Brand Email:-> {brandEmail}.

    The Verification Team will look into your request and get back to you in the next 48 hours.

    If this request was not initiated by you reachout to any of our admin on
    {[user.email for user in User.objects.filter(is_staff=True, is_superuser=True)[:3]]}
    """
    try:
        send_mail(
            subject,
            body,
            "tailor'sconnect@noreply.com",
            [userEmail],
            fail_silently=False
        )
    except:
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
            [user.email for user in User.objects.filter(is_staff=True, is_superuser=True)[:3]],
            fail_silently=False
        )
    except ConnectionError:
        return False

    return True
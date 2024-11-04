from django.core.mail import send_mail
# from django.conf import settings
from authUser.models import User
from celery import shared_task

##### design Request #######
@shared_task
def DesignRequestEmail(userEmail:str, brandName:str, brandEmail:str) -> bool:
    subject = "Request Received"
    body = f"""do not reply this mail
    
    Hello {userEmail};
    Your request for creating a designer profile with the following details is recieved.

    Brand Name:-> {brandName}.
    Brand Email:-> {brandEmail}.

    The Verification Team will look into your request and get back to you in the next 48 hours.

    If this request was not initiated by you reach out to any of our admin on
    
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
    except ConnectionError:
        return False
    return True

###### email verification for designers ########
@shared_task
def DesignerVerifyEmail(demail) -> bool:
    subject = "Designer Verification Request"
    body = f"""
    A new user with email {demail} is requesting to be verified as a designer.

    Check his profile and do the needful
    """
    try:
        send_mail(
            subject,
            body,
            demail,
            [user.email for user in User.objects.filter(is_staff=True, is_superuser=True)],
            fail_silently=False
        )
    except ConnectionError:
        return False

    return True

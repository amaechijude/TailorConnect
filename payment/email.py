from celery import shared_task
from django.core.mail import send_mail

company_email = "tailor'sconnect@noreply.com"

@shared_task
def initiate_order_email(user_email:str, style_name:str, amount):
    """
    Email sent at order initiation
    """
    subject = "Order Initiation"
    body = f"""
        You have initiated an order to buy {style_name} at the price of {amount}.

        Please do well to complete your payment on time for fast delivery.

        Thank you for your purchase
    """
    try:
        send_mail(
            subject,
            body,
            company_email,
            user_email,
            fail_silently=False
        )
    except ConnectionError:
        return
    return

@shared_task
def order_payment_confirmation(parameter_list):
    """
    docstring
    """
    pass



@shared_task
def initiate_donation_email(donor_email:str, amount:str):
    """
    email that is sent on donation initiation
    """
    subject = "Donation"
    body = f"""
    We really want to appreciate you for donating the sum of  {amount} naira.
    This humoungous amount will go a long way for us.

    Thank you very much.
    """
    try:
        send_mail(
            subject,
            body,
            company_email,
            [donor_email],
            fail_silently=False
        )
    except ConnectionError:
        return False
    return True
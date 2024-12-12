from celery import shared_task
from django.core.mail import send_mail

company_email = "tailor'sconnect@noreply.com"

@shared_task
def initiate_order_email(user_email: str, style_name: str, amount: float) -> None:
    """
    Sends an email to the user upon initiating an order.

    Parameters:
    user_email (str): The email address of the user placing the order.
    style_name (str): The name of the style or product being ordered.
    amount (float): The total cost of the order.

    Returns:
    None: This function does not return any value. It sends an email to the user.
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
            [user_email],
            fail_silently=False
        )
    except ConnectionError:
        return
    return

@shared_task
def order_payment_confirmation_email(user_email: str, style_title: str, order_amount: str, order_ref: str) -> None:
    """
    Sends an email to the user upon successful payment verification.

    Parameters:
    user_email (str): The email address of the user who made the payment.
    style_title (str): The title or name of the style or product purchased.
    order_amount (str): The total cost of the order.
    order_ref (str): The unique reference number of the order.

    Returns:
    None: This function does not return any value. It sends an email to the user.
    """
    subject = "Order Payment Confirmation"
    body = f"""
        Your payment of the sum of {order_amount} for {style_title} has been confirmed.
        Your order reference number is {order_ref}. Your purchase will be delivered at the appointed time.

        Thanks for your patronage.
    """
    try:
        send_mail(
            subject,
            body,
            company_email,
            [user_email],
            fail_silently=False
        )
    except ConnectionError:
        return
    return



@shared_task
def initiate_donation_email(donor_email: str, amount: str) -> None:
    """
    Sends an email to the donor upon initiating a donation.

    Parameters:
    donor_email (str): The email address of the donor.
    amount (str): The amount donated by the donor in naira.

    Returns:
    None: This function does not return any value. It sends an email to the donor.

    The function constructs an email with a subject "Donation" and a body that thankfully acknowledges the donation.
    It then attempts to send the email using Django's send_mail function. If a ConnectionError occurs during the email sending process,
    the function returns without raising an exception.
    """
    subject = "Donation"
    body = f"""
    We really want to appreciate you for donating the sum of {amount} naira.
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
        return
    return
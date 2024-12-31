import pprint
from django.shortcuts import render, get_object_or_404
# from django.conf import settings
from django.contrib.auth.decorators import login_required
from creators.models import Style
from payment.ercaspay import Ercaspay
# from .paystack import Paystack
from authUser.models import ShippingAddress, Measurement
from django.contrib import messages
from .models import Order, Payment, Donations
# from authUser.forms import mForm
from django.http import HttpResponse, JsonResponse
from rest_framework import status
# import requests
# from pprint import pprint
from .email import initiate_donation_email, initiate_order_email, order_payment_confirmation_email
# Create your views here.

@login_required(login_url="login_user")
def initiate_order(request):
    """
    This function handles the process of initiating a new order. It checks if the request method is POST,
    retrieves necessary data from the request, creates a new Order object, and sends an email notification.

    Parameters:
    request (HttpRequest): The incoming request object containing POST data.

    Returns:
    HttpResponse: If the request method is not POST, returns an HttpResponse with a message indicating the method not supported.
    render: If the request method is POST, creates a new Order object, sends an email notification, and renders the 'payment/make_payment.html' template with the new order details.
    """
    if request.method != 'POST':
        return HttpResponse("Method not supported")
    styleId = request.POST.get('styleId')
    shipId = request.POST.get('shipId')
    m_id = request.POST.get("m_id")

    measurement = get_object_or_404(Measurement, id=m_id)
    style = get_object_or_404(Style, id=styleId)
    shipp = ShippingAddress.objects.get(id=shipId, user=request.user) if request.user.is_authenticated else None
    amount = round(float(style.asking_price), 2)
    user = request.user
    new_order = Order.objects.create(
        user=user,style=style,shipp_addr=shipp,
        amount=amount, measurement=measurement
        )
    new_order.save()
    initiate_order_email.delay_on_commit(new_order.user.email, new_order.style.title, new_order.amount)
    return render(request, 'payment/make_payment.html', {"order": new_order})


##### pay ####
def pay(request):
    """
    Handles the payment initiation process for an order. It checks if the user is authenticated and if the request method is POST.
    Retrieves the order based on the provided order ID, initiates a transaction with Ercaspay, and returns the checkout URL and transaction reference.

    Parameters:
    request (HttpRequest): The incoming request object containing POST data.

    Returns:
    JsonResponse: If the user is not authenticated, returns a JSON response with an error message and HTTP 401 status.
    JsonResponse: If the request method is not POST, returns a JSON response with an error message and HTTP 405 status.
    HttpResponse: If the order does not exist, returns an HTTP response with an error message.
    JsonResponse: If the transaction initiation is successful, returns a JSON response with the checkout URL and transaction reference.
    HttpResponse: If the payment request fails, returns an HTTP response with an error message and HTTP 400 status.
    """
    if not request.user.is_authenticated:
        return HttpResponse({"error": "You need to login"}, status=status.HTTP_401_UNAUTHORIZED) 
    if request.method != 'POST':
        return HttpResponse({"error": "Method not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    pk = request.POST.get("orderId")
    try:
        order = get_object_or_404(Order, id=pk)
        amount = float(order.style.asking_price)
    except Order.DoesNotExist:
        return HttpResponse("Order no longer exist")

    ercas = Ercaspay()
    response = ercas.Initiate_transaction(amount, order.payment_refrence, order.user.name, order.user.email, descrption=f"payment for {order.style.title}")
    if response.status_code not in [200, 201, 202]:
        return HttpResponse(f"error: Payment Initiation Request not succesful {response.json()}")
    pprint.pprint(response.json())
    response_data = response.json()
    if response_data["requestSuccessful"] and response_data["responseCode"] == "success":
        response_body = response_data["responseBody"]
        chekout_url = response_body["checkoutUrl"]
        transaction_ref = response_body["transactionReference"]

        get_payment, new_payment = Payment.objects.get_or_create(order=order, amount=amount, payment_refrence=order.payment_refrence,
                                                                 transaction_refrence=transaction_ref)
        order_in = get_payment.order
        order_in.transaction_refrence = transaction_ref
        order_in.status = Order.Status.Processing
        order_in.save()

        return JsonResponse({"chekout_url":chekout_url, "transaction_reference":transaction_ref})
    return HttpResponse({"error": "Payment request failed"}, status=status.HTTP_400_BAD_REQUEST)


####### Verify Payment
def verify_payment(request):
    ref = request.GET.get("reference")
    if ref is None:
        return HttpResponse("Payment  verification Incomplete")
    ercas = Ercaspay()
    verify = ercas.Verify_transaction(transaction_ref=ref)
    if verify is True:
        payment = Payment.objects.get(transaction_refrence=ref)
        order = payment.order
        payment.verified = True
        payment.save()
        order.status = Order.Status.Successful
        order.save()
        order_payment_confirmation_email.delay_on_commit(order.user.email, order.style.title, order.amount, order.ref)
        messages.info(request, "Payment Verification Successful")
        return render(request, "payment/success.html")
    return HttpResponse("Verification failed")

#### Donate ####
def donate(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        amnt = request.POST.get("amount")
        new_donation = Donations.objects.create(name=name, email=email, amount=round(float(amnt), 2))
        new_donation.save()
        ercas = Ercaspay()
        response = ercas.Initiate_transaction(new_donation.amount, new_donation.payment_refrence, new_donation.name, new_donation.email, descrption="A goodwill donation")
        if response.status_code not in [200, 201]:
            return HttpResponse({"error": "Request not succesful"})

        response_data = response.json()
        if response_data["requestSuccessful"] and response_data["responseCode"] == "success":
            response_body = response_data["responseBody"]
            chekout_url = response_body["checkoutUrl"]
            transaction_ref = response_body["transactionReference"]
            initiate_donation_email.delay_on_commit(new_donation.email, new_donation.amount)
            return JsonResponse({"chekout_url":chekout_url, "transaction_reference":transaction_ref})
        return HttpResponse({"error": "Payment request failed"}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"error": "Method not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

####### Verify Donations #####
def verify_donations(request):
    ref = request.GET.get("reference")
    if ref is None:
        return HttpResponse("Payment  verification Incomplete")
    ercas = Ercaspay()
    verify = ercas.Verify_transaction(ref)
    if verify is True:
        donation = Donations.objects.get(transactiom_refrence=ref)
        donation.verified = True
        donation.save()
        messages.info(request, "Donation Verification Successful")
        return render(request, "payment/success.html")
    return HttpResponse("Verification Failed")
    

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from creators.models import Style
from .paystack import Paystack
from authUser.models import ShippingAddress, Measurement
from django.contrib import messages
from .models import Order, Payment, Donations
# from authUser.forms import mForm
from django.http import HttpResponse, JsonResponse
from rest_framework import status
import requests
from pprint import pprint
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
    if request.user.is_authenticated:  
        if request.method != 'POST':
            return JsonResponse({"error": "Method not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        pk = request.POST.get("orderId")
        try:
            order = get_object_or_404(Order, id=pk)
            amount = float(order.style.asking_price)
        except:
            return HttpResponse("Order no longer exist")
        
        ps = Paystack()
        response = ps.Initiate_transaction(f"{request.user.email}", amount)
        if response.status_code != 200:
            return JsonResponse({"error": "Request not succesful"}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = response.json()
        
        access_code = response_data["data"]["access_code"]
        ref = response_data["data"]["reference"]

        get_payment, new_payment = Payment.objects.get_or_create(order=order,ref=ref, amount=order.style.asking_price)
        order_in = get_payment.order
        order_in.status = Order.Status.Processing
        order_in.save()

        return JsonResponse({"access_code": access_code,"ref":ref},status=status.HTTP_200_OK)
    return JsonResponse({"error": "You need to login"}, status=status.HTTP_401_UNAUTHORIZED)
    

####### Verify Payment
def verify_payment(request):
    ref = request.GET.get("reference")
    if ref is None:
        return HttpResponse("Payment  verification Incomplete")
    ps = Paystack()
    verify = ps.verify_transaction(ref)
    if verify["status"] == True:
        va = float(verify["data"]["amount"])
        payment = Payment.objects.get(ref=ref)
        order = payment.order
        if (va / 100) == float(payment.amount):
            payment.verified = True
            payment.save()
            order.status = Order.Status.Successful
            order.save()
            order_payment_confirmation_email.delay_on_commit(order.user.email, order.style.title, order.amount, order.ref)
            messages.info(request, "Payment Verification Successful")
            return render(request, "payment/success.html")
        return HttpResponse("Amount Mismatch")
    return HttpResponse(f"{verify['message']}")
    

#### Donate ####
def donate(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        amnt = request.POST.get("amount")
        amount = round(float(amnt), 2)
        ps = Paystack()
        response = ps.Initiate_transaction(email, amount)

        if response.status_code != 200:
            return JsonResponse({"error": "Request not succesful"}, status=status.HTTP_400_BAD_REQUEST)
    
        response_data = response.json()
        access_code = response_data["data"]["access_code"]
        ref = response_data["data"]["reference"]
        new_donation = Donations.objects.create(email=email, amount=amount, ref=ref)
        new_donation.save()
        initiate_donation_email.delay_on_commit(email, str(amnt))
        return JsonResponse({"access_code": access_code,"ref":ref},status=status.HTTP_200_OK)
    return JsonResponse({"error": "Method not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

####### Verify Donations #####
def verify_donations(request):
    ref = request.GET.get("reference")
    if ref is None:
        return HttpResponse("Payment  verification Incomplete")
    ps = Paystack()
    verify = ps.verify_transaction(ref)
    if verify["status"] == True:
        va = float(verify["data"]["amount"])
        donation = Donations.objects.get(ref=ref)
        if (va / 100) == float(donation.amount):
            donation.verified = True
            donation.save()
            messages.info(request, "Payment Verification Successful")
            return render(request, "payment/success.html")
        return HttpResponse("Amount Mismatch")
    return HttpResponse(f"{verify['message']}")
    

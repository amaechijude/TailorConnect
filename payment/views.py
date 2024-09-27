from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from designs.models import Style
from authUser.models import ShippingAddress, Measurement
# from django.contrib import messages
from .models import Order, Payment
from authUser.forms import mForm
from django.http import HttpResponse, JsonResponse
from rest_framework import status
import requests
from pprint import pprint
# Create your views here.

@login_required(login_url="login_user")
def initiate_order(request):
    if request.method == 'POST':
        styleId = request.POST.get('styleId')
        shipId = request.POST.get('shipId')
        m_id = request.POST.get("m_id")
    
        measurement = get_object_or_404(Measurement, id=m_id)
        style = get_object_or_404(Style, id=styleId)
        shipp = ShippingAddress.objects.get(id=shipId, user=request.user) if request.user.is_authenticated else None
        amount = style.asking_price
    
        new_order = Order.objects.create(
            user=request.user,style=style,
            shipp_addr=shipp, amount=amount,
            measurement=measurement
            )
        new_order.save()

        context = {
            "order": new_order.style
            }
        return render(request, 'payment/make_payment.html', context)
    return HttpResponse("Get method not supported")
    # return render(request, 'payment/initiate.html')


##### pay ####
def pay(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pk = request.POST.get("orderId")
            try:
                order = get_object_or_404(Order, id=pk)
                amount = float(order.style.asking_price) * 100
            except:
                return HttpResponse("Order no longer exist")
            
            sk = settings.PAYSTACK_SECRET_KEY
            url = "https://api.paystack.co/transaction/initialize"

            headers = {
                "Authorization": f"Bearer {sk}",
                "Content-Type": "application/json"
                }
            data = {
                "email": f"{request.user.email}",
                "amount": f"{amount}"
                }

            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()

            pprint(response_data)
            
            access_code = response_data["data"]["access_code"]
            ref = response_data["data"]["reference"]
            
            new_payment = Payment.objects.create(order=order,ref=ref, amount=order.style.asking_price)
            new_payment.save()

            return JsonResponse({"access_code": access_code,"ref":ref},status=status.HTTP_200_OK)
        return HttpResponse("Get method not supported")
    return HttpResponse("You need to login")

      

def verify_payment(request, ref):
    verify_status = verifyFunction(ref=ref)
    if verify_status:
        payment = Payment.objects.get(ref=ref)
        payment.verified = True
        payment.save()
        return render(request, "payment/success.html")
    return render(request, "payment/success.html")


def verifyFunction(ref):
	paystack_sk = settings.PAYSTACK_SECRET_KEY
	url = f"https://api.paystack.co/transaction/verify/{ref}"
	headers = {
		"Authorisation": f"Bearer {paystack_sk}"
	}
	response = requests.get(url=url, headers=headers)
	response_data = response.json()
	status = response_data["status"]
	# amount = response_data["data"]
	return status

# {
#   "status": true,
#   "message": "Authorization URL created",
#   "data": {
#     "authorization_url": "https://checkout.paystack.com/nkdks46nymizns7",
#     "access_code": "nkdks46nymizns7",
#     "reference": "nms6uvr1pl"
#   }
# }

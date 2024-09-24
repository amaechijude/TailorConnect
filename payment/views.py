from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from designs.models import Style
from authUser.models import ShippingAddress
# from django.contrib import messages
from .models import Order, Payment
from designs.forms import mForm
from django.http import HttpResponse
import requests as req
from pprint import pprint
# Create your views here.

def initiate_order(request):
    if request.method == 'POST':
        mform = mForm(request.POST, request.FILES or None)
        if mform.is_valid():
            styleId = request.POST.get('styleId')
            shipId = request.POST.get('shipId')
            measurement = mform.cleaned_data['measurement']
        # try:
        
            style = get_object_or_404(Style, id=styleId)
            shipp = ShippingAddress.objects.get(id=shipId, user=request.user) if request.user.is_authenticated else None
            amount = style.asking_price
            paystack_pub_key = settings.PAYSTACK_PUBLIC_KEY
        
            new_order = Order.objects.create(
                user=request.user,style=style,
                shipp_addr=shipp, amount=amount,
                measurement=measurement
                )
            new_order.save()
            payment = Payment.objects.create(order=new_order, amount= new_order.amount)

            context = {
                "style": style
                }
            return render(request, 'payment/make_payment.html', context)
        return HttpResponse(f"{mform.errors}")
    return HttpResponse("Get method not supported")
    # return render(request, 'payment/initiate.html')


##### pay ####
@login_required(login_url="login_user")
def pay(request):
    if request.method == 'POST':
        pk = request.POST.get("styleId")
        try:
            style = get_object_or_404(Style, id=pk)
            amount = int(style.asking_price) * 100
        except:
            return HttpResponse("Item no longer exist")
        
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

        response = req.post(url, headers=headers, json=data)
        response_data = response.json()
        
        access_code = response_data["data"]["access_code"]
        pprint(access_code)

        return render(request, 'payment/continue.html', {"access_code": access_code})
    return HttpResponse("Get method not supported")

      

def verify_payment(request, ref):
	payment = Payment.objects.get(ref=ref)
	verified = payment.verify_payment()

	if verified:
        #   Process order logic
		return render(request, "payment/success.html")
	return render(request, "payment/success.html")



# {
#   "status": true,
#   "message": "Authorization URL created",
#   "data": {
#     "authorization_url": "https://checkout.paystack.com/nkdks46nymizns7",
#     "access_code": "nkdks46nymizns7",
#     "reference": "nms6uvr1pl"
#   }
# }
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from designs.models import Style
from authUser.models import ShippingAddress
from django.contrib import messages
from .models import Order, Payment
from designs.forms import mForm
# Create your views here.

def initiate_order(request):
    if request.method == 'POST':
        form = mForm(request.POST, request.FILES)
        if form.is_valid():
            styleId = request.POST.get('styleId')
            shipId = request.POST.get('shipId')
            measurement = form.cleaned_data['measurement']
        # try:
        
        style = get_object_or_404(Style, id=styleId)
        shipp = ShippingAddress.objects.filter(user=request.user).first()
        amount = style.asking_price
        paystack_pub_key = settings.PAYSTACK_PUBLIC_KEY
        # except:
        #     messages.error(request, "Item does not exist")
        #     return redirect('index')
        
        new_order = Order.objects.create(
            user=request.user,style=style, shipp_addr=shipp, amount=amount,
            measurement=measurement,)
        new_order.save()
        payment = Payment.objects.create(order=new_order, amount= new_order.amount)

        context = {
			'payment': payment,
			'field_values': request.POST,
			'paystack_pub_key': paystack_pub_key,
			'amount_value': payment.amount_value(),
            }
        return render(request, 'payment/make_payment.html', context)
    return render(request, 'payment/initiate.html')


def verify_payment(request, ref):
	payment = Payment.objects.get(ref=ref)
	verified = payment.verify_payment()

	if verified:
        #   Process order logic
		return render(request, "payment/success.html")
	return render(request, "payment/success.html")




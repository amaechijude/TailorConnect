from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail



def index(request):
    designers = Designer.verified.all()
    styles = Style.published.all()
    category = Category.objects.all()
    context = {
        "designers": designers,
        "styles": styles,
        'category': category,
    }
    return render(request, 'core/index.html', context)


def cartView(request):
    return render(request, 'core/cart.html')

def checkout(request):
    return render(request, 'core/checkout.html')

def contact(request):
    return render(request, 'core/contact.html')

def detail(request):
    return render(request, 'core/detail.html')

def shop(request):
    return render(request, 'core/shop.html')

def status(request):
    return render(request, 'core/status.html')

def designer(request, pk):
    ds = Designer.verified.get(id=pk)
    return render(request, 'core/designer.html', {'ds':ds})


def category(request, pk):
    cat = Category.objects.filter(id=pk)
    return render(request, 'core/category.html', {'cat': cat})




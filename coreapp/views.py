from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            messages.info(request, f"Your account is created with eamil {str(email)} You can now login")
            return redirect('login_user')
        return redirect('login_user')
    form = RegisterForm()
    return render(request, 'account/signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user != None:
                messages.info(request, f"You are logged in")
                login(request, user)
                return redirect('index')
            messages.error(request, f"Account not found")
            return redirect('login_user')
        
        messages.error(request, f"{form.errors}")
        return redirect('login_user')
    
    if request.user.is_authenticated:
        messages.info(request, f"You are logged in already")
        return redirect('index')
    
    form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    messages.error(request, f"You are logged out")
    return redirect('login_user')

def profile(request):
    return render(request, 'account/profile')



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
    return render(request, 'core/box.html')

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




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import RegisterForm, LoginForm
from django.contrib import messages

User = get_user_model

def chat(request):
    return render(request, 'auth/chat.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create(email=email, password=password)
            message = messages.info(request, f"Your account is created with eamil {user.email} You can now login")
            return redirect('login', {"message": message})
        return redirect('login')
    form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user != None:
                login(request, user)
                return redirect('index')
            return redirect('login')
        return redirect('login')
    form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')
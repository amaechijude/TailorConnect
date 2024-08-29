from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "password1"}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "Confirm password1"}))



class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password= forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}))


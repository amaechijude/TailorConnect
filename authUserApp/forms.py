from django import forms
# from django.contrib.auth.forms import UserCreationForm

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"id":"email", "class":"form-control","placeholder":"Enter your Email"}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"id":"subject", "class":"form-control", "placeholder": "password1"}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"id":"subject", "class":"form-control", "placeholder": "Confirm password1"}))



class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"id":"email", "class":"form-control","placeholder":"Enter your Email"}))
    password= forms.CharField(required=True, widget=forms.PasswordInput(attrs={"id":"subject", "class":"form-control", "placeholder": "Enter password"}))


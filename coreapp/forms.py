from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"id":"email", "class":"form-control","placeholder":"Enter your Email"}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"id":"password1","autocomplete": True, "class":"form-control", "placeholder": "password"}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"id":"password2", "autocomplete": True, "class":"form-control", "placeholder": "Confirm password"}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"id":"email", "class":"form-control","placeholder":"Enter your Email"}))
    password= forms.CharField(required=True, widget=forms.PasswordInput(attrs={"id":"password", "autocomplete": True, "class":"form-control", "placeholder": "Enter password"}))


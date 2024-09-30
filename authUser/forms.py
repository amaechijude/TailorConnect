from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ShippingAddress, Measurement

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

fclass = "form-control"

class ShippingAddressForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id": "first_name", "class": fclass
        }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id": "last_name", "class": fclass
        }))
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id":"address", "class":fclass
        }))
    zip_code = forms.CharField(required=True, max_length=7, widget=forms.NumberInput(attrs={
        "id": "zip_code", "class": fclass
        }))

    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'address', 'zip_code']


class MeasurementForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id":"title", "class":fclass, "placeholder":"Title"
    }))
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={
        "id": "body", "class":fclass, "rows":3, "placeholder":"Measurement"
    }))
    class Meta:
        model = Measurement
        fields = ['title', 'body']

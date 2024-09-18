from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from creators.models import Designer

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

fclass="form-control"

class CreateDesignerForm(forms.ModelForm):
    brand_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id": "brand_name", "class": fclass
        }))
    brand_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "id":"brand_email", "class":fclass
    }))
    # brand_phone = forms.CharField(required=True, max_length=14, widget=forms.TextInput(attrs={
    #     "id": "brand_phone", "class": fclass,
    #     }))
    brand_logo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "id": "brand_logo", "class": fclass,
    }))
    brand_bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "id": "brand_bio", "class":fclass, "rows":3
    }))
    brand_location = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id":"brand_location", "class":fclass,
    }))
    google_map_url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "id":"google_map_url", "class":fclass
    }))
    website_url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "id":"website_url", "class":fclass
    }))
    instagram_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "id":"instagram_link", "class":fclass
    }))
    twitter_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "id":"twitter_link", "class":fclass
    }))
    facebook_link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "id":"facebook_link", "class":fclass
    }))

    class Meta:
        model = Designer
        exclude = ('user', 'joined_on')
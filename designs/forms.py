from django import forms
from .models import Style

class StyleForm(forms.ModelForm):
    class Meta:
        model = Style
        fields = ['title', 'description', 'images', 'can_request', 'asking_price', 'status']

class updateStyleForm(forms.ModelForm):
    class Meta:
        model = Style
        fields = ['title', 'description', 'images', 'can_request', 'asking_price', 'status']

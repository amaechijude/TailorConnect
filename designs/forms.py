from django import forms
from .models import Style, Review

fclass = "form-control"

class StyleForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id": "title", "class": fclass
        }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "id": "description", "class":fclass, "rows":3
    }))
    images = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "id": "images", "class": fclass,
    }))
    can_request = forms.ChoiceField(choices=Style.rStatus, widget=forms.Select(attrs={
        "id": "can_request", "class": fclass,
    }))
    asking_price = forms.DecimalField(required=True, max_digits=9999999999, decimal_places=2, widget=forms.NumberInput(
        attrs={"id":"asking_price"}
    ))
    status = forms.ChoiceField(choices=Style.Status, widget=forms.Select(attrs={
        "id": "status", "class": fclass,
    }))
    class Meta:
        model = Style
        fields = ['title', 'description', 'images', 'can_request', 'asking_price', 'status']


class updateStyleForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id": "title", "class": fclass
        }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "id": "description", "class":fclass, "rows":3
    }))
    images = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "id": "images", "class": fclass,
    }))
    can_request = forms.ChoiceField(choices=Style.rStatus, widget=forms.Select(attrs={
        "id": "can_request", "class": fclass,
    }))
    asking_price = forms.DecimalField(required=True, max_digits=9999999999, decimal_places=2, widget=forms.NumberInput(
        attrs={"id":"asking_price"}
    ))
    status = forms.ChoiceField(choices=Style.Status, widget=forms.Select(attrs={
        "id": "status", "class": fclass,
    }))
    class Meta:
        model = Style
        fields = ['title', 'description', 'images', 'can_request', 'asking_price', 'status']


######## Review form ######
class ReviewForm(forms.ModelForm):
    text_content = forms.CharField(required=False, widget=forms.Textarea(attrs={"id": "brand_bio", "class":fclass, "rows":3 }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"id": "brand_logo", "class": fclass,}))
    
    class Meta:
        model = Review
        fields = ['text_content', 'image']


from django import forms
from .models import Style, Review

fclass = "form-control"

class StyleForm(forms.ModelForm):
    class Meta:
        model = Style
        fields = ['title', 'description', 'images', 'can_request', 'asking_price', 'status']

class updateStyleForm(forms.ModelForm):
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
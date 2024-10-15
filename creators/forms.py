from django import forms
from .models import Designer, Style, Review

fclass="form-control"

class CreateDesignerForm(forms.ModelForm):
    brand_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id": "brand_name", "class": fclass
        }))
    brand_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "id":"brand_email", "class":fclass
    }))
    # brand_phone = forms.CharField(required=True, max_length=14, widget=forms.NumberInput(attrs={
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
        exclude = ('user', 'is_verified', 'joined_on', 'brand_phone')


class UpdateBrandForm(forms.ModelForm):
    brand_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id": "brand_name", "class": fclass
        }))
    brand_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "id":"brand_email", "class":fclass
    }))
    # brand_phone = forms.CharField(required=True, max_length=14, widget=forms.NumberInput(attrs={
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
        exclude = ('user', 'is_verified', 'joined_on', 'brand_phone')



fclass = "form-control"

class StyleForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id": "title", "class": fclass
        }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "id": "description", "class":fclass, "rows":3
    }))
    thumbnail = forms.ImageField(required=True, widget=forms.FileInput(attrs={
        "id": "thumbnail", "class": fclass,
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
        fields = ['title', 'description', 'thumbnail', 'can_request', 'asking_price', 'status']


class updateStyleForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "id": "title", "class": fclass
        }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "id": "description", "class":fclass, "rows":3
    }))
    thumbnail = forms.ImageField(required=True, widget=forms.FileInput(attrs={
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
        fields = ['title', 'description', 'thumbnail', 'can_request', 'asking_price', 'status']


######## Review form ######
class ReviewForm(forms.ModelForm):
    text_content = forms.CharField(required=False, widget=forms.Textarea(attrs={"id": "brand_bio", "class":fclass, "rows":3 }))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"id": "brand_logo", "class": fclass,}))
    
    class Meta:
        model = Review
        fields = ['text_content', 'image']


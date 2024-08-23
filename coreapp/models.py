from django.db import models
from shortuuid import ShortUUID
from django_resized import ResizedImageField
from django.core.validators import URLValidator

from datetime import timezone,datetime
utc_time = datetime.now(timezone.utc)

from django.conf import settings
User = settings.AUTH_USER_MODEL

def get_user_email(instance):
    user_email = '{0}'.format(instance.user.email)
    return user_email

def user_dir_path(instance, filename) -> str:
    user_dir = 'user_{0}/{1}'.format(instance.user.email, filename)
    return str(user_dir)

##### Category like shirt skirt etc#######
class Category(models.Model):
    name = models.CharField(max_length=150)
    thumbnail = ResizedImageField(quality=60, upload_to="Categories")
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


##### Designers, Tailors, Stylists etc ########
class Designer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    brand_name= models.CharField(max_length=150, blank=False)
    brand_email = models.EmailField(default=get_user_email)
    brand_logo = ResizedImageField(quality=60, upload_to=f"Designers/{user_dir_path}", blank=True, null=True)
    location = models.CharField(max_length=150, default="here")
    google_map = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    other_online_link = models.URLField(blank=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.brand_name}"
    class Meta:
        verbose_name = "Designer"
        verbose_name_plural = "Designers"

###### Designs, styles, creations etc. #######
class Style(models.Model):
    designer = models.ForeignKey(Designer, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    images = ResizedImageField(quality=60, upload_to=f"Styles/{user_dir_path}")

    can_request = models.BooleanField(default=False)
    asking_price = models.DecimalField(max_digits=9999999999, decimal_places=2, default=0.99)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(utc_time)

    def __str__(self) -> str:
        return f"{self.name} --- created_by  {self.designer.brand_name}"
    
    class Meta:
        verbose_name = "Style"
        verbose_name_plural = "Styles"
    

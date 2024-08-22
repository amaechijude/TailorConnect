from django.db import models
from shortuuid import ShortUUID
from django_resized import ResizedImageField
# Create your models here.
from django.conf import settings
User = settings.AUTH_USER_MODEL

def get_user_email(instance):
    return f"{instance.user.email}"

def user_dir_path(instance, filename):
    return f"{instance.user.email}/{filename}"

class Designer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    brand_name= models.CharField(max_length=150, blank=False)
    brand_email = models.EmailField(default=get_user_email)
    brand_logo = ResizedImageField(quality=60, upload_to="Designers", blank=True, null=True)

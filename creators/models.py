from django.db import models
from django_resized import ResizedImageField
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class DesignerManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_verified=Designer.Status.YES)
##### Designers, Tailors, Stylists etc ########
class Designer(models.Model):
    class Status(models.TextChoices):
        NO = 'NO', 'No'
        YES = 'YES', 'YES'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name= models.CharField(max_length=150, blank=False, unique=True)
    brand_email = models.EmailField(unique=True)
    brand_logo = ResizedImageField(quality=60, size=[100, 150], crop=['middle', 'center'], upload_to=f"Designers", blank=True, null=True)
    brand_bio = models.TextField(default="description")
    brand_location = models.CharField(max_length=150, default="here")
    brand_phone = models.CharField(max_length=14)
    google_map_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    is_verified = models.CharField(max_length=4, choices=Status, default=Status.NO)

    objects = models.Manager()
    verified = DesignerManager()

    def __str__(self) -> str:
        return f"{self.brand_name}"
    class Meta:
        verbose_name = "Designer"
        verbose_name_plural = "Designers"


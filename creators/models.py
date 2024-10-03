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



#### Style Manager
class StyleManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Style.Status.PUBLISHED)
###### Designs, styles, creations etc. #######
class Style(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    class rStatus(models.TextChoices):
        No = "NO", "NO"
        YES = "YES", "YES"

    designer = models.ForeignKey(Designer, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    thumbnail = ResizedImageField(blank=False, null=False, quality=60, size=[1080, 1080], crop=['middle', 'center'], upload_to="Styles")
    likes = models.PositiveIntegerField(default=0)
    num_of_reviews = models.PositiveIntegerField(default=0)

    can_request = models.CharField(max_length=4, choices=rStatus, default=rStatus.No)
    asking_price = models.DecimalField(max_digits=9999999999, decimal_places=2, default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=5, choices=Status, default=Status.DRAFT)
    objects = models.Manager()
    published = StyleManager()

    def __str__(self) -> str:
        return f"{self.title} --- created_by  {self.designer.brand_name}"
    
    class Meta:
        verbose_name = "Style"
        verbose_name_plural = "Styles"


###### Reviews for styles#####
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    text_content = models.TextField()
    image = ResizedImageField(quality=60, size=[1000, 1080], crop=['middle', 'center'], upload_to="Reviews")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Review on {self.style.title}"
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

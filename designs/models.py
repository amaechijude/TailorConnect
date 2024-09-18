from django.db import models
from creators.models import Designer, ResizedImageField, User
# Create your models here.


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
    images = ResizedImageField(quality=60, upload_to=f"Styles")
    likes = models.PositiveIntegerField(default=0)
    num_of_reviews = models.PositiveIntegerField(default=0)

    can_request = models.CharField(max_length=4, choices=rStatus, default=rStatus.No)
    asking_price = models.DecimalField(max_digits=9999999999, decimal_places=2, default=0.99)
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
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Review on {self.style.title}"
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

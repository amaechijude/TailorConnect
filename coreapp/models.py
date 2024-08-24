from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django_resized import ResizedImageField
from django.core.validators import URLValidator

from datetime import timezone,datetime
utc_time = datetime.now(timezone.utc)
from django.conf import settings

# def get_user_email(instance):
#     user_email = '{0}'.format(instance.user.email)
#     return user_email

# def user_dir_path(instance, filename) -> str:
#     user_dir = 'user_{0}/{1}'.format(instance.user.email, filename)
#     return str(user_dir)


SHIPPING_STATUS = (
    ("packaging", "packaging"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered")
)

STAR_RATINGS = (
    (1, "☆☆☆☆★"),
    (2, "☆☆☆★★"),
    (3, "☆☆★★★"),
    (4, "☆★★★★"),
    (5, "★★★★★"),
)

User = settings.AUTH_USER_MODEL
##### Designers, Tailors, Stylists etc ########
class Designer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    brand_name= models.CharField(max_length=150, blank=False)
    brand_email = models.EmailField()
    brand_logo = ResizedImageField(quality=60, upload_to=f"Designers", blank=True, null=True)
    location = models.CharField(max_length=150, default="here")
    google_map = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    other_online_link = models.URLField(blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.brand_name}"
    class Meta:
        verbose_name = "Designer"
        verbose_name_plural = "Designers"


##### Category like shirt skirt etc#######
class Category(models.Model):
    name = models.CharField(max_length=150)
    thumbnail = ResizedImageField(quality=60, upload_to="Categories", blank=True, null=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


###### Designs, styles, creations etc. #######
class Style(models.Model):
    sytleId = ShortUUIDField(primary_key=True, unique=True, max_length=35, prefix="style", editable=False)
    designer = models.ForeignKey(Designer, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    images = ResizedImageField(quality=60, upload_to=f"Styles")
    likes = models.PositiveBigIntegerField(default=0)
    num_of_reviews = models.PositiveBigIntegerField(default=0)

    can_request = models.BooleanField(default=False)
    asking_price = models.DecimalField(max_digits=9999999999, decimal_places=2, default=0.99)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(utc_time)

    def __str__(self) -> str:
        return f"{self.name} --- created_by  {self.designer.brand_name}"
    
    class Meta:
        verbose_name = "Style"
        verbose_name_plural = "Styles"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    text_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Review on {self.style.title}"
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=False)
    phone = models.CharField(max_length=13, help_text="+234")
    address1 = models.CharField(max_length=150, blank=False)
    address2 =models.CharField(max_length=150, blank=True, help_text="Optional")
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10)


class Order(models.Model):
    orderId = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    designer = models.ForeignKey(Designer, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=9999999999999, decimal_places=2)
    shippingStatus = models.CharField(max_length=50,choices=SHIPPING_STATUS, default=SHIPPING_STATUS[0])
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __strr__(self) -> str:
        return f"Ordered by {self.user.email} -- on {self.created_at}"
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


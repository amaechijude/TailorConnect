from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django_resized import ResizedImageField



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extrafields):
        if not email:
            raise ValueError("Email cant be empty")
        if not password:
            raise ValueError("Provide password")
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extrafields):
        extrafields.setdefault("is_staff", True)
        extrafields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extrafields)
    
    def get_by_natural_key(self, email: str):
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin):
    userId = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=False,null=True, blank=True, default="user")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    avatar = ResizedImageField(quality=60,upload_to=f"Users", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    wishlist_count = models.PositiveIntegerField(default=0)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"
    class Meta:
        verbose_name_plural = "Users"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    phone = models.CharField(max_length=13, help_text="+234")
    address = models.CharField(max_length=150, blank=False)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=150)
    lga = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10)


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
    brand_logo = ResizedImageField(quality=60, upload_to=f"Designers", blank=True, null=True)
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


##### Category like shirt skirt etc#######
class Category(models.Model):
    name = models.CharField(max_length=150)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


#### Style Manager
class StyleManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Style.Status.PUBLISHED)
###### Designs, styles, creations etc. #######
class Style(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    designer = models.ForeignKey(Designer, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    images = ResizedImageField(quality=60, upload_to=f"Styles")
    likes = models.PositiveIntegerField(default=0)
    num_of_reviews = models.PositiveIntegerField(default=0)

    can_request = models.BooleanField(default=False)
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


####### order items ###################
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(Style)

    def __str__(self) -> str:
        return f"Wishlist of {self.user.email}"
    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    
####### order items ###################
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
    shippingaddress = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=9999999999, decimal_places=2)
    measurement = ResizedImageField(quality=60, upload_to=f"Measurement")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Ordered by {self.user.email} -- on {self.created_at}"
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


###### Payment #######
class Payment(models.Model):
    class Status(models.TextChoices):
        Processing = 'Processing', 'Processing'
        Successful = 'Successful', 'Successful'
        Cancelled = 'Cancelled', 'Cancelled'

    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=99999999999, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status, default=Status.Processing)
    date_initiated = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for order {self.order}"
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


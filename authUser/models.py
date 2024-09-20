from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django_resized import ResizedImageField
from designs.models import Style

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
    name = models.CharField(max_length=150, unique=False,null=True, blank=True)
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


####### order items ###################
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(Style)

    def __str__(self) -> str:
        return f"Wishlist of {self.user.email}"
    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

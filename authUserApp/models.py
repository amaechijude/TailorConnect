from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from shortuuid.django_fields import ShortUUIDField

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
    userId = ShortUUIDField(max_length=35, prefix="user", primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"
    class Meta:
        verbose_name_plural = "Users"
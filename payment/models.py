from enum import unique
from django.db import models
from django.conf import settings
from authUser.models import ShippingAddress, Measurement
from creators.models import Style
from uuid6 import uuid7
import base64

import payment

User = settings.AUTH_USER_MODEL

def short_uuid7():
    """
    Generates a short Base64 encoded string from a UUIDv7.

    This function creates a UUIDv7 and encodes it into a URL-safe Base64 string,
    removing any trailing '=' characters.

    Returns:
        str: A short Base64 encoded string representation of a UUIDv7.
    """
    return base64.urlsafe_b64encode(uuid7().bytes).decode('utf-8').rstrip("=")

####### order items ###################
class Order(models.Model):
    class Status(models.TextChoices):
        Processing = 'Processing', 'Processing'
        Successful = 'Successful', 'Successful'
        Cancelled = 'Cancelled', 'Cancelled'
        Delivered = 'Delivered', 'Delivered'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
    shipp_addr = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=12, choices=Status, default=Status.Processing)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_refrence = models.CharField(max_length=50, default=short_uuid7, unique=True, editable=False, blank=False)
    transaction_refrence = models.CharField(max_length=300, blank=True)

    def __str__(self) -> str:
        return f"Ordered by {self.user.email} -- on {self.created_at}"
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


###### Payment #######
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_refrence = models.CharField(max_length=50, blank=True)
    transaction_refrence = models.CharField(max_length=300, blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self):
        return f"Payment: {self.amount}"


class Donations(models.Model):
    name = models.CharField(max_length=300, blank=True)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_refrence = models.CharField(max_length=50, default=short_uuid7, unique=True, editable=False, blank=False)
    transaction_refrence = models.CharField(max_length=300, blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date_created',)
    
    def __str__(self):
        return f"{self.email}  donated {self.amount} on {self.date_created}"


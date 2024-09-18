from django.db import models
from django_resized import ResizedImageField
from django.conf import settings
from authUser.models import ShippingAddress
from designs.models import Style
User = settings.AUTH_USER_MODEL

    
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


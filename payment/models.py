from django.db import models
from django_resized import ResizedImageField
from django.conf import settings
from authUser.models import ShippingAddress
from designs.models import Style
from .paystack import Paystack
import secrets

User = settings.AUTH_USER_MODEL

   
####### order items ###################
class Order(models.Model):
    class Status(models.TextChoices):
        Processing = 'Processing', 'Processing'
        Successful = 'Successful', 'Successful'
        Cancelled = 'Cancelled', 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
    shipp_addr = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=12, choices=Status, default=Status.Processing)
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
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	amount = models.DecimalField(max_digits=999999999999, decimal_places=2)
	ref = models.CharField(max_length=300)
	verified = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-date_created',)

	def __str__(self):
		return f"Payment: {self.amount}"

	def save(self, *args, **kwargs):
		while not self.ref:
			ref = secrets.token_urlsafe(50)
			object_with_similar_ref = Payment.objects.filter(ref=ref)
			if not object_with_similar_ref:
				self.ref = ref

		super().save(*args, **kwargs)
	
	def amount_value(self):
		return int(self.amount) * 100

	def verify_payment(self):
		paystack = Paystack()
		status, result = paystack.verify_payment(self.ref, self.amount)
		if status:
			if result['amount'] / 100 == self.amount:
				self.verified = True
			self.save()
		if self.verified:
			return True
		return False
	
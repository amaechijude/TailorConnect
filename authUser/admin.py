from django.contrib import admin
from .models import ShippingAddress, User, WishList, Measurement
# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(User)
admin.site.register(WishList)
admin.site.register(Measurement)


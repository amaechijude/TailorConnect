from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Designer)
admin.site.register(Style)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(ShippingAddress)
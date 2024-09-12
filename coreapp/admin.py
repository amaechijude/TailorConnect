from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Designer)
admin.site.register(Style)
admin.site.register(Review)
admin.site.register(OrderItems)
admin.site.register(ShippingAddress)
admin.site.register(Category)
admin.site.register(User)
from django.urls import path
from . import views

urlpatterns = [
    path('initiate', views.initiate_order, name='initiate_order'),
    path('pay', views.pay, name='pay'),
    path('verify', views.verify_payment, name='verify_payment'),
    path('donate', views.donate, name='donate'),
    path('donate/verify', views.verify_donations, name='donate_verify'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart', views.cartView, name='cart'),
    path('contact', views.contact, name='contact'),
    path('detail', views.detail, name='detail'),
    path('shop', views.shop, name='shop'),
    path('checkout', views.checkout, name='checkout'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('initiate', views.initiate_order, name='initiate_order'),
    path('verify/<str:ref>', views.verify_payment, name='verify_payment')
]
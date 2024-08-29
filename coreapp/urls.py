from django.urls import path
from . import api
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api', api.home, name='home'),
    path('api/styles/create', api.createStyle, name="createStyle"),
    path('api/designer/create', api.create_designer, name='create_designer'),
    path('api/review/create/<str:pk>', api.create_review, name='review'),
    # path('home', views.home, name='home')
]

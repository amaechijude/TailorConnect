from django.urls import path
from. import views

urlpatterns = [
    path('', views.styles, name='styles'),
    path('designer', views.designer, name="designer"),
    path('designer/create', views.create_designer, name='create_designer'),
    path('review/create/<str:pk>', views.create_review, name='review'),
    # path('home', views.home, name='home')
]

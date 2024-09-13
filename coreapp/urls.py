from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('signup/', views.register, name='register'),
    path('wishlist/<int:pk>', views.AddWishlist, name="wishlist"),
    path('profile', views.profile, name='profile'),
    # path('cart', views.cartView, name='cart'),
    path('contact', views.contact, name='contact'),
    path('detail', views.detail, name='detail'),
    path('shop', views.shop, name='shop'),
    path('checkout', views.checkout, name='checkout'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('signup/', views.register, name='register'),
    path('wishlist', views.wishlist, name="wishlist"),
    path('add_wishlist/<int:pk>', views.AddWishlist, name="add_wishlist"),
    path('rm_wishlist/<int:pk>', views.RemoveWishlist, name='rm_wishlist'),
    path('shop', views.dshop, name='dshop'),
    path('designer/<int:pk>', views.designers, name='designer'),
    path('createDesign', views.createDesign, name='createDesign'),
    path('profile', views.profile, name='profile'),
    path('profile/address', views.shippingAddr, name='shipping'),
    path('product/<int:pk>', views.product, name='product'),
    path('addReview', views.addReview, name='addReview'),
    # path('cart', views.cartView, name='cart'),
    # path('contact', views.contact, name='contact'),
]

from django.urls import path
from . import views
from authUser import views as aviews
from creators import views as cviews
from designs import views as dviews

urlpatterns = [
    path('', views.index, name='index'), # index
    path('login', aviews.login_user, name='login_user'), #login
    path('logout', aviews.logout_user, name='logout_user'), #logo out
    path('signup', aviews.register, name='register'), # Register /Signup
    path('profile', aviews.profile, name='profile'),
    path('profile/address', aviews.shippingAddr, name='shipping'),
    path('wishlist', aviews.wishlist, name="wishlist"), #Wishlist
    path('add_wishlist/<int:pk>', aviews.AddWishlist, name="add_wishlist"), # Add wishlist
    path('rm_wishlist/<int:pk>', aviews.RemoveWishlist, name='rm_wishlist'), # Remove Wishlist
    path('shop', views.dshop, name='dshop'), 
    path('designer/<int:pk>', cviews.designers, name='designer'),
    path('createDesign', cviews.createDesign, name='createDesign'),
    path('product/<int:pk>', dviews.product, name='product'),
    path('addReview', dviews.addReview, name='addReview'),
    path('createStyle', dviews.createStyle, name="createStyle"),
    # path('cart', views.cartView, name='cart'),
    # path('contact', views.contact, name='contact'),
]

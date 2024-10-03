from django.urls import path
from . import views
from authUser import views as aviews
from creators import views as cviews

urlpatterns = [
    path('', views.index, name='index'), # index
    path('login', aviews.login_user, name='login_user'), #login
    path('logout', aviews.logout_user, name='logout_user'), #logo out
    path('signup', aviews.register, name='register'), # Register /Signup
    path('profile', aviews.profile, name='profile'),
    path('profile/address', aviews.shippingAddr, name='shipping'),
    path('profile/measurement', aviews.addMeasurement, name='measurement'),
    path('wishlist', aviews.wishlist, name="wishlist"), #Wishlist
    path('add_wishlist/<int:pk>', aviews.AddWishlist, name="add_wishlist"), # Add wishlist
    path('rm_wishlist/<int:pk>', aviews.RemoveWishlist, name='rm_wishlist'), # Remove Wishlist
    path('shop', cviews.dshop, name='dshop'), 
    path('designer/<int:pk>', cviews.designers, name='designer'),
    path('createDesigner', cviews.createDesigner, name='createDesigner'),
    path('updateBrand', cviews.updateBrand, name='updateBrand'),
    path('product/<int:pk>', cviews.product, name='product'),
    path('addReview', cviews.addReview, name='addReview'),
    path('createStyle', cviews.createStyle, name="createStyle"),
    path('updateStyle', cviews.updateStyle, name='updateStyle'),
    
]

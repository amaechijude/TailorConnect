from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as st
from rest_framework.response import Response
import json
from asgiref.sync import sync_to_async

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            messages.info(request, f"Your account is created with eamil {str(email)} You can now login")
            return redirect('login_user')
        return redirect('login_user')
    form = RegisterForm()
    return render(request, 'account/signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user != None:
                messages.info(request, f"You are logged in")
                login(request, user)
                return redirect('index')
            messages.error(request, f"Account not found")
            return redirect('login_user')
        
        messages.error(request, f"{form.errors}")
        return redirect('login_user')
    
    if request.user.is_authenticated:
        messages.info(request, f"You are logged in already")
        return redirect('index')
    
    form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    messages.error(request, f"You are logged out")
    return redirect('login_user')

####### index ##########
def index(request):
    st = Style.published.all().order_by("-created_at")
    page_number = request.GET.get('page', 1)
    st_paginator = Paginator(st, 20)
    styles = st_paginator.get_page(page_number)
    category = Category.objects.all()
    context = {
        "styles": styles,
        'category': category,
    }
    return render(request, 'core/index.html', context)


####wishlist view ######
@login_required(login_url='login_user')
def wishlist(request):
    wishl = WishList.objects.filter(user=request.user).first()
    styles = wishl.members.all()
    return render(request, 'core/wishlist.html', {"styles": styles})

####### add wishlist ######
def AddWishlist(request, pk):
    if request.user.is_authenticated:
       user=request.user
       style = Style.objects.get(id=pk)
       wish, created = WishList.objects.get_or_create(user=user)

       if wish.members.filter(id=style.id).exists():
           return JsonResponse({"exist": "Already in your wishlist"}, status=st.HTTP_200_OK)
       
       wish.members.add(style)
       user.wishlist_count += 1
       user.save()
       return JsonResponse({"add": "Added to wishlist", "wcount": user.wishlist_count}, status=st.HTTP_201_CREATED)
    
    return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)

#### remove wishlist ########
def RemoveWishlist(request, pk):
    if request.user.is_authenticated:
       user=request.user
       style = Style.objects.get(id=pk)
       wish = WishList.objects.get(user=request.user)

       if wish.members.filter(id=style.id).exists():
           wish.members.remove(style)
           if user.wishlist_count <= 0:
               pass
           else:
               user.wishlist_count -= 1
               user.save()
           return JsonResponse({"removed": "Removed from your wishlist", "wcount": request.user.wishlist_count}, status=st.HTTP_200_OK)
       
       return JsonResponse({"not": "item not in your wishlist"}, status=st.HTTP_200_OK)
    
    return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)


###### designers page ########
def designers(request, pk):
    ds = Designer.verified.get(id=pk)
    styles = Style.published.filter(designer=ds)
    context = {"ds":ds, "styles": styles}
    return render(request, 'core/designer.html', context)

###### profile page ########
@login_required(login_url='login_user')
def profile(request):
    user = request.user
    shipaddr = ShippingAddress.objects.filter(user=user).first()
    wishl = WishList.objects.filter(user=request.user).first()
    if wishl is None:
        styles = None
    else:
        styles = wishl.members.all().order_by("-created_at")[:2]
    context = {"user": user, "shipaddr": shipaddr, "sty": styles}
    return render(request, 'account/profile.html', context)

###### add shipping address ########
def shippingAddr(request):
    if request.user.is_authenticated:
        # body = request.body.decode("utf-8")
        # data = json.loads(data)
        user = request.user
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        country = request.POST.get("country")
        state = request.POST.get("state")
        lga = request.POST.get("lga")
        zip_code = request.POST.get("zip_code")
        
        new_ship = ShippingAddress.objects.create(
            user=user,first_name=first_name, last_name=last_name,
            phone=phone, address=address,
            country=country, state=state,lga=lga, zip_code=zip_code
            )
        new_ship.save()
        return JsonResponse({"added": "Added shipping address"})

    return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)

##### design shop customisation etc #####
@login_required(login_url='login_user')
def dshop(request):
    user = request.user
    ds = Designer.verified.get(user=user)
    styles = Style.published.filter(designer=ds)
    context = {"ds":ds, "styles": styles}
    return render(request, 'core/box.html', context)

##### Create Design ####
@login_required(login_url='login_user')
def createDesign(request):
    if request.method == 'POST':
        if request.user.designer:
            messages.info(request, "You can only create one design shop")
            return redirect('profile')
        
        brand_name = request.POST.get("brand_name")
        brand_email = request.POST.get("brand_email")
        brand_logo = request.FILES.get("brand_logo")
        brand_bio = request.POST.get("brand_bio")
        brand_location = request.POST.get("brand_location")
        brand_phone = request.POST.get("brand_phone")
        google_map_url =request.POST.get("google_map_url")
        website_url = request.POST.get("website_url")
        instagram_link = request.POST.get("instagram_link")
        twitter_link =request.POST.get("twitter_link")
        facebook_link = request.POST.get("facebook_link")

        new_designer = Designer.objects.create(
            user=request.user, brand_name=brand_name, brand_email=brand_email,
            brand_logo=brand_logo, brand_bio=brand_bio, brand_location=brand_location,
            brand_pnone=brand_phone, google_map_url=google_map_url, website_url=website_url,
            instagram_link=instagram_link, twitter_link=twitter_link, facebook_link=facebook_link
        )
        new_designer.save()
        ##### send a mail to admins informig them to verify new designers #######
        messages.info(request, "Created")
        return redirect('profile')


def status(request):
    return render(request, 'core/status.html')


def category(request, pk):
    cat = Category.objects.filter(id=pk)
    return render(request, 'core/category.html', {'cat': cat})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, ShippingAddressForm
from django.contrib import messages
from .models import WishList, ShippingAddress, Measurement
from creators.models import Style
from creators.forms import CreateDesignerForm
from payment.models import Order
from django.http import JsonResponse, HttpResponse
from rest_framework import status as st
from django_ratelimit.decorators import ratelimit
from django.core.paginator import Paginator
####### register ######
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']
            WishList.objects.create(user=user)
            messages.info(request, f"Your account is created with eamil {str(email)} You can now login")
            return redirect('login_user')

        return HttpResponse(f"{form.errors}")

    form = RegisterForm()
    return render(request, 'account/signup.html', {'form': form})

##### Login view ###s
#@ratelimit(key="user_or_ip", rate="5/m")
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                messages.info(request, "You are logged in")
                return redirect('index')
            messages.error(request, "Account not found")
            return redirect('login_user')
        
        return HttpResponse(f"{form.errors}")
    
    if request.user.is_authenticated:
        messages.info(request, "You are logged in already")
        return redirect('index')
    
    form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


##### Logout view #####
@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    messages.info(request, "You are logged out")
    return redirect('login_user')


####wishlist view ######
#@cache_page(60 * 10) # 60 seconds * 10 == 10 mins
@login_required(login_url='login_user')
def wishlist(request):
    wishlist = WishList.objects.filter(user=request.user).first()
    styles = wishlist.members.all() if wishlist else None
    
    return render(request, 'core/wishlist.html', {"styles": styles})

####### add wishlist ######
#@ratelimit(key='user_or_ip', rate='3/s')
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
#@ratelimit(key="user_or_ip", rate="3/s")
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
           return JsonResponse({"removed": "Removed from your wishlist", "wcount": user.wishlist_count}, status=st.HTTP_200_OK)
       return JsonResponse({"not": "item not in your wishlist"}, status=st.HTTP_200_OK)
    return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)

###### profile page ########
#@cache_page(60 * 5) # 5 minutes
@login_required(login_url='login_user')
def profile(request):
    user = request.user
    shipaddr = ShippingAddress.objects.filter(user=user).first()
    wishl = WishList.objects.filter(user=request.user).first()
    styles = wishl.members.all().order_by("-created_at")[:2] if wishl else None
    orders = Order.objects.filter(user=user).order_by('-created_at')[:2]
    form = CreateDesignerForm()
    sform = ShippingAddressForm()
    context = {"user":user, "shipaddr":shipaddr, "sty":styles, "form":form, "sform":sform, "orders":orders}
    return render(request, 'account/profile.html', context)

###### add shipping address ########
@login_required(login_url='login_user')
def shippingAddr(request):
    if request.method == 'POST':
        sform = ShippingAddressForm(request.POST)
        if sform.is_valid():
            new_addr = sform.save(commit=False)

            new_addr.user = request.user
            new_addr.phone = request.POST.get("phone")
            new_addr.counttry = request.POST.get("country")
            new_addr.state = request.POST.get("state")
            new_addr.lga = request.POST.get("lga")

            new_addr.save()
            messages.success(request,"Shipping Added")
            return redirect('profile')
        return HttpResponse(f"{sform.errors}")
    return HttpResponse("Bad request")


@login_required(login_url='login_user')
def addMeasurement(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get("title")
        body = request.POST.get("body")
        ms = Measurement.objects.create(user=user, title=title, body=body)
        ms.save()
        messages.success(request,"Measurement Added")
        return redirect('profile')
    return HttpResponse("Invalid Method")


@login_required(login_url='login_user')
@cache_page(60 * 3)
def list_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by("-created_at")
    context = {"orders": orders}
    return render(request, 'account/orders.html', context)

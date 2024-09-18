from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, CreateDesignerForm
from django.contrib import messages
from .models import WishList, ShippingAddress
from designs.models import Style
from django.http.response import JsonResponse
from rest_framework import status as st

####### register ######
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            messages.info(request, f"Your account is created with eamil {str(email)} You can now login")
            return redirect('login_user')

        messages.error(request, f"{form.errors}")
        return redirect('register')
    form = RegisterForm()
    return render(request, 'account/signup.html', {'form': form})

##### Login view ###s
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


##### Logout view #####
@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    messages.info(request, f"You are logged out")
    return redirect('login_user')


####wishlist view ######
@login_required(login_url='login_user')
def wishlist(request):
    wishl = WishList.objects.filter(user=request.user).first()
    styles = wishl.members.all() if wishl else None
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



###### profile page ########
@login_required(login_url='login_user')
def profile(request):
    user = request.user
    shipaddr = ShippingAddress.objects.filter(user=user).first()
    wishl = WishList.objects.filter(user=request.user).first()
    styles = wishl.members.all().order_by("-created_at")[:2] if wishl else None
    form = CreateDesignerForm()
    context = {"user": user, "shipaddr": shipaddr, "sty": styles, "form": form}
    return render(request, 'account/profile.html', context)

###### add shipping address ########
def shippingAddr(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                user = request.user
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            country = request.POST.get("country")
            state = request.POST.get("state")
            lga = request.POST.get("lga")
            zip_code = request.POST.get("zip_code")
        
            new_ship.save()
            return JsonResponse({"added": "Added shipping address"})

    return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)

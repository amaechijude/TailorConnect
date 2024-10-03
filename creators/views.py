from django.shortcuts import render, redirect, get_object_or_404
from .models import Designer, Style, Review
from authUser.models import WishList, Measurement, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import status as st
from django.http import HttpResponse, JsonResponse
from .forms import UpdateBrandForm, CreateDesignerForm, ReviewForm, StyleForm, updateStyleForm
# Create your views here.

###### designers page ########
def designers(request, pk):
    ds = Designer.objects.get(id=pk)
    styles = Style.published.filter(designer=ds)
    if request.user.is_authenticated:
        wishl = WishList.objects.filter(user=request.user).first() or None
        sty = wishl.members.all() or None
    else:
        sty = None
    context = {"ds":ds, "styles": styles, "sty":sty}
    return render(request, 'core/designer.html', context)


##### designer profile shop customisation etc #####
@login_required(login_url='login_user')
def dshop(request):
    try:
        ds = get_object_or_404(Designer, user=request.user)
    except:
        messages.info(request, "You don't have a designer profile")
        return redirect('profile')
    
    styles = Style.objects.filter(designer=ds).order_by("-created_at")
    form = StyleForm()
    uform = UpdateBrandForm(instance=ds)
    context = {"ds":ds, "styles": styles, "form": form, "uform": uform}
    
    return render(request, 'core/dshop.html', context)
   
   
##### Create Design ####
@login_required(login_url='login_user')
def createDesigner(request):
    if request.method == 'POST':
        try:
            ds = Designer.objects.get(user=request.user)
            messages.info(request, "You can only create one design shop")
            return redirect('dshop')
        except:
            form = CreateDesignerForm(request.POST, request.FILES)
            if form.is_valid():
                new_designer = form.save(commit=False)
                new_designer.user = request.user
                new_designer.brand_phone = request.POST.get("brand_phone")
                new_designer.save()
                ##### send a mail to admins informing them to verify new designers #######
                messages.info(request, "Created")
                return redirect('dshop')
            
            return HttpResponse(f"{form.errors}")
    return HttpResponse("Invalid Method")

####### Update Brand Details #############
@login_required(login_url="login_user")
def updateBrand(request):
    if request.method == 'POST':
        try:
            ds = Designer.objects.get(user=request.user)
        except:
            return HttpResponse("You don't have a designer profile")
        uform = UpdateBrandForm(request.POST, request.FILES or None, instance=ds)
        if uform.is_valid():
            update = uform.save(commit=False)
            update.user = request.user
            update.brand_phone = request.POST.get("brand_phone")
            update.save()
            messages.info(request, "Brand details Updated")
            return redirect('dshop')
        
        return HttpResponse(f"{uform.errors}")
    return HttpResponse("Invalid Method")
        

#### Product details ######
def product(request, pk):
    style = Style.objects.get(id=pk)
    reviews = Review.objects.filter(style=style).order_by("-created_at")
    usform = updateStyleForm(instance=style)
    rform = ReviewForm()
    if request.user.is_authenticated:
        wishl = WishList.objects.filter(user=request.user).first()
        sty = wishl.members.all() if wishl else None
        shipaddr = ShippingAddress.objects.filter(user=request.user)
        measure = Measurement.objects.filter(user=request.user)
    else:
        sty = None
        shipaddr = None
        measure = None
    
    context =  {
        "style": style, "reviews": reviews, "sty":sty, "measure": measure,
        "usform":usform, "rform":rform, "shipaddr": shipaddr,
        }
    return render(request, 'core/product.html', context)


###### create styles #############
@login_required(login_url='login_user')
def createStyle(request):
    if request.method == 'POST':
        try:
            ds = get_object_or_404(Designer, user=request.user)
        except:
            return HttpResponse("You don't have a designer profile")
        form = StyleForm(request.POST, request.FILES or None)
        if form.is_valid():
            new_style = form.save(commit=False)
            new_style.designer = ds
            new_style.save()
            return redirect('dshop')
        return HttpResponse(f"{form.errors}")
    return HttpResponse("Method not allowed")
    
###### Update styles #############
@login_required(login_url='login_user')
def updateStyle(request):
    if request.method == 'POST':
        try:
            ds = get_object_or_404(Designer, user=request.user)
        except:
            return HttpResponse("You don't have a designer profile")
        
        usform = StyleForm(request.POST, request.FILES or None)
        if usform.is_valid():
            styleUpdate = usform.save(commit=False)
            styleUpdate.designer = ds
            styleUpdate.save()
            
            return redirect('dshop')
        return HttpResponse(f"{usform.errors}")
    return HttpResponse("Method not allowed")

###### add review #############
def addReview(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            #process logic
            rform = ReviewForm(request.POST, request.FILES or None)
            if rform.is_valid():
                new_review = rform.save(commit=False)
                styleid = request.POST.get('styleid')
                name = request.POST.get('name')
                user = request.user
                user.name = name; user.save()
                style = Style.objects.get(id=styleid)
                new_review.user = user
                new_review.style = style
                new_review.save()

                context = {
                    'user': new_review.user.name,
                    'content': new_review.text_content,
                    'date': new_review.created_at
                }
            
                return JsonResponse(context, status=st.HTTP_200_OK)
            return HttpResponse(f"{rform.errors}")
        return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)
    return JsonResponse({"method": "Method not allowed"}, status=st.HTTP_405_METHOD_NOT_ALLOWED)


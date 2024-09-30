from django.shortcuts import render, redirect, get_object_or_404
from designs.models import Designer, Style
from authUser.models import WishList
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from designs.forms import StyleForm
from .forms import UpdateBrandForm, CreateDesignerForm
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
        ds = get_object_or_404(Designer, user=request.user)# Designer.objects.get(user=request.user)
    except:
        messages.info(request, "You don't have a vendor profile")
        return redirect('profile')
    
    styles = Style.objects.filter(designer=ds)
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

####### Update Brand Details #############
@login_required(login_url="login_user")
def updateBrand(request):
    if request.method == 'POST':
        try:
            ds = Designer.objects.get(user=request.user)
            uform = UpdateBrandForm(request.POST, request.FILES or None, instance=ds)
            if uform.is_valid():
                update = uform.save(commit=False)
                update.user = request.user
                update.brand_phone = request.POST.get("brand_phone")
                update.save()
                messages.info(request, "Brand details Updated")
                return redirect('dshop')
            
            return HttpResponse(f"{uform.errors}")
        except:
            messages.error(request, "You don't have a vendor profile")
            return redirect('index')
        
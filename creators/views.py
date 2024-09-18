from django.shortcuts import render, redirect
from designs.models import Designer, Style
from authUser.models import WishList
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authUser.forms import CreateDesignerForm
from designs.forms import StyleForm
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
        ds = Designer.objects.get(user=request.user)
        styles = Style.objects.filter(designer=ds)
        form = StyleForm()
        context = {"ds":ds, "styles": styles, "form": form}
        return render(request, 'core/dshop.html', context)
    except:
        messages.info(request, "You don't have a vendor profile")
        return redirect('profile')


##### Create Design ####
@login_required(login_url='login_user')
def createDesigner(request):
    if request.method == 'POST':
        try:
            ds = Designer.objects.get(user=request.user)
            messages.info(request, "You can only create one design shop")
            return redirect('profile')
        except:
            form = CreateDesignerForm(request.POST, request.FILES)
            if form.is_valid():
                new_designer = form.save(commit=False)
                new_designer.user = request.user
                new_designer.brand_phone = request.POST.get("brand_phone")
                new_designer.save()
                ##### send a mail to admins informing them to verify new designers #######
                messages.info(request, "Created")
                return redirect('profile')
            
            messages.info(request, f"{form.errors}")
            return redirect('profile')



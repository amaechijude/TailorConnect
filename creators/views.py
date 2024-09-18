from django.shortcuts import render, redirect
from designs.models import Designer, Style
from authUser.models import WishList
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authUser.forms import CreateDesignerForm

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



##### Create Design ####
@login_required(login_url='login_user')
def createDesign(request):
    if request.method == 'POST':
        try:
            ds = Designer.objects.get(user=request.user)
            messages.info(request, "You can only create one design shop")
            return redirect('profile')
        except:
            form = CreateDesignerForm(request.POST, request.FILES)
            if form.is_valid():
                new_designer = form.save(commit=False)
                brand_phone = request.POST.get("brand_phone")
                new_designer.user = request.user
                new_designer.brand_phone=brand_phone
                new_designer.is_verified = "No"
                new_designer.save()
                ##### send a mail to admins informig them to verify new designers #######
                messages.info(request, "Created")
                return redirect('profile')
            
            messages.info(request, f"{form.errors}")
            return redirect('profile')


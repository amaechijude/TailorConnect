from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authUser.models import WishList
from creators.models import Designer
from designs.models import Style

####### index ##########
def index(request):
    st = Style.published.all().order_by("-created_at")
    page_number = request.GET.get('page', 1)
    st_paginator = Paginator(st, 20)
    styles = st_paginator.get_page(page_number)
    if request.user.is_authenticated:
        wishl = WishList.objects.filter(user=request.user).first() or None
        sty = wishl.members.all() if wishl else None
    else:
        sty = None
    context = {
        "styles": styles,
        "sty": sty
    }
    return render(request, 'core/index.html', context)


##### design shop customisation etc #####
@login_required(login_url='login_user')
def dshop(request):
    try:
        ds = Designer.objects.get(user=request.user)
        styles = Style.published.filter(designer=ds)
        context = {"ds":ds, "styles": styles}
        return render(request, 'core/designer.html', context)
    except:
        messages.info(request, "You don't have a vendor profile")
        return redirect('profile')








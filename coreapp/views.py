from django.shortcuts import render
from django.core.paginator import Paginator
from authUser.models import WishList
from creators.models import Style
from django.views.decorators.cache import cache_page

####### index ##########
#@cache_page(60 * 10)
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

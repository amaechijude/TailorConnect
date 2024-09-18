from django.shortcuts import render
from .models import Style, Review
from authUser.models import WishList
from django.http.response import JsonResponse
from rest_framework import status as st
# Create your views here.

#### Product details ######
def product(request, pk):
    style = Style.objects.get(id=pk)
    reviews = Review.objects.filter(style=style)
    if request.user.is_authenticated:
        wishl = WishList.objects.filter(user=request.user).first() or None
        sty = wishl.members.all() or None
    else:
        sty = None
    return render(request, 'core/product.html', {"style": style, "reviews": reviews, "sty":sty})


###### add review #############
def addReview(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return JsonResponse({"rev": "Review added"}, status=st.HTTP_201_CREATED)
        return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)
    return JsonResponse({"bad": "Bad Request"}, status=st.HTTP_400_BAD_REQUEST)

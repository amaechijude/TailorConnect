from django.shortcuts import render
from .models import Style, Review
from authUser.models import WishList
from django.http.response import JsonResponse
from rest_framework import status as st
from .forms import StyleForm
# Create your views here.

#### Product details ######
def product(request, pk):
    style = Style.objects.get(id=pk)
    reviews = Review.objects.filter(style=style)
    if request.user.is_authenticated:
        wishl = WishList.objects.filter(user=request.user).first() or None
        sty = wishl.members.all() if wishl else None
    else:
        sty = None
    return render(request, 'core/product.html', {"style": style, "reviews": reviews, "sty":sty})


###### create styles #############
def createStyle(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            #process form logic
            form = StyleForm(request.POST, request.FILES or None)
            if form.is_valid():
                new_style = form.save(commit=False)
                new_style.designer = request.user.designer
                form.save()
                return JsonResponse({"add": "style created"}, status=st.HTTP_201_CREATED)
            
            return JsonResponse({"error": f"{form.errors}"}, statu=st.HTTP_400_BAD_REQUEST)
        return JsonResponse({"method": "Method not allowed"}, status=st.HTTP_405_METHOD_NOT_ALLOWED)
    return JsonResponse({"err": "You need to login"}, statu=st.HTTP_401_UNAUTHORIZED)


###### add review #############
def addReview(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            #process logic
            
            return JsonResponse({"rev": "Review added"}, status=st.HTTP_201_CREATED)
        return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)
    return JsonResponse({"method": "Method not allowed"}, status=st.HTTP_405_METHOD_NOT_ALLOWED)


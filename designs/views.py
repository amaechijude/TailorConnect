from django.shortcuts import render
from .models import Style, Review
from authUser.models import WishList
from django.http.response import JsonResponse
from rest_framework import status as st
from .forms import StyleForm, updateStyleForm, ReviewForm
# Create your views here.

#### Product details ######
def product(request, pk):
    style = Style.objects.get(id=pk)
    reviews = Review.objects.filter(style=style).order_by("-created_at")
    usform = updateStyleForm(instance=style)
    rform = ReviewForm()
    if request.user.is_authenticated:
        wishl = WishList.objects.filter(user=request.user).first() or None
        sty = wishl.members.all() if wishl else None
    else:
        sty = None
    
    context =  {
        "style": style, "reviews": reviews, "sty":sty, "usform":usform, "rform":rform
        }
    return render(request, 'core/product.html', context)


###### create styles #############
def createStyle(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            #process form logic
            form = StyleForm(request.POST, request.FILES or None)
            if form.is_valid():
                new_style = form.save(commit=False)
                new_style.designer = request.user.designer
                new_style.save()
                context = {
                        'designer': new_style.designer.brand_name,
                        'title': new_style.title,
                        'description': new_style.description,
                        'images': new_style.images.url,
                        'price': new_style.asking_price
                        }
                return JsonResponse(context, status=st.HTTP_201_CREATED)
            
            return JsonResponse({"error": f"{form.errors}"}, statu=st.HTTP_400_BAD_REQUEST)
        return JsonResponse({"method": "Method not allowed"}, status=st.HTTP_405_METHOD_NOT_ALLOWED)
    return JsonResponse({"err": "You need to login"}, statu=st.HTTP_401_UNAUTHORIZED)

def updateStyle(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            #process form logic
            usform = StyleForm(request.POST, request.FILES or None)
            if usform.is_valid():
                styleUpdate = usform.save(commit=False)
                styleUpdate.designer = request.user.designer
                styleUpdate.save()
                return JsonResponse({"add": "style created"}, status=st.HTTP_201_CREATED)
            return JsonResponse({"error": f"{usform.errors}"}, statu=st.HTTP_400_BAD_REQUEST)
        return JsonResponse({"method": "Method not allowed"}, status=st.HTTP_405_METHOD_NOT_ALLOWED)
    return JsonResponse({"err": "You need to login"}, statu=st.HTTP_401_UNAUTHORIZED)

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
            
                return JsonResponse(context, status=st.HTTP_201_CREATED)
            return JsonResponse({"formerr": f"{rform.errors}"})
        return JsonResponse({"err": "You need to login"}, status=st.HTTP_401_UNAUTHORIZED)
    return JsonResponse({"method": "Method not allowed"}, status=st.HTTP_405_METHOD_NOT_ALLOWED)


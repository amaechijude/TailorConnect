from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .serializer import *

#rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


@api_view(['GET'])
def home(request):
    s = Style.objects.all()
    ss = StyleSerializer(s, many=True)
    ds = Designer.objects.all()
    dss = DesignerSerializer(ds, many=True)
    ok = {
        "styles": ss.data,
        "designers": dss.data
    }
    return Response(ok, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_designer(request):
    serializer = DesignerSerializer(data=request.data)
    if serializer.is_valid():
        d = serializer.save(user=request.user)
        user_response = {
            "message": "Designer successfully created",
            "Designer": {
                "name": d.brand_name,
                "email": d.brand_email,

            }
        }
        return Response(user_response, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createStyle(request):
    serializer = StyleSerializer(data=request.data)
    if serializer.is_valid():
        s = serializer.save(designer=request.user.designer)
        d = {
            "success": "success"
        }
        return Response(d, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
    # user_response = {"message": "Unauthorised Request"}
    # return Response(user_response, status.HTTP_401_UNAUTHORIZED)    

@api_view(['POST'])
@permission_classes(IsAuthenticated)
def create_review(request, pk):
    style = Style.objects.filter(styleId=pk)
    serializer = ReviewSerializer(data=request.data)
    if style is not None:
        if serializer.is_valid():
            s = serializer.save(user=request.user, style=style)
            return(s.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Permission Denied"}, status.HTTP_401_UNAUTHORIZED)




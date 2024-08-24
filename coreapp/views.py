from django.shortcuts import render
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
def designer(request):
    ds = Designer.objects.all()
    dss = DesignerSerializer(ds, many=True)
    return JsonResponse(dss.data, safe=False)


@api_view(['GET'])
def styles(request):
    s = Style.objects.all()
    ss = StyleSerializer(s, many=True)
    return Response(ss.data, status.HTTP_200_OK)


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
    user = request.user
    serializer = StyleSerializer(data=request.data)
    designer = Designer.objects.filter(user=user).first()
    if designer is not None:
        if serializer.is_valid():
            s = serializer.save(designer=designer)

            return Response(s.data, status.HTTP_201_CREATED)
        return(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
    user_response = {"message": "Unauthorised Request"}
    return Response(user_response, status.HTTP_401_UNAUTHORIZED)    

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





from django.shortcuts import render
from django.http.response import JsonResponse
from .serializer import DesignerSerializer, Designer
#rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

def home(request):
    return JsonResponse({
        "home":"welcome"
    })

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def designer(request):
    if request.method == 'POST':
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
    
    ds = Designer.objects.all()
    dss = DesignerSerializer(ds, many=True)
    return JsonResponse(dss.data, safe=False)

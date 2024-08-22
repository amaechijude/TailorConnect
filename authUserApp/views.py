from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import UserSerializer
# Create your views here.

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_token_for_user(user)
            output = {
                "Message": "Registration successfull", 

                "data": {
                    "userId": user.userId,
                    "email": user.email
                    },
                "token": {
                    "refresh_token": token["refresh_token"],
                    "access_token": token["access_token"]
                }
            }
            return Response(output, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def login_user(request):
    if request.user.is_authenticated:
        return Response({"login": "Done"}, status.HTTP_200_OK)
    
    return Response({"error": "You need to log in"}, status.HTTP_401_UNAUTHORIZED)

def logout_user(request):
    return JsonResponse({
        "logout": "Coming soon"
    })


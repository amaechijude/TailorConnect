from django.shortcuts import render
from django.http.response import JsonResponse

#rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
def home(request):
    return JsonResponse({
        "home":"welcome"
    })

def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh_token": refresh,
        "access_token": refresh.access_token
        }
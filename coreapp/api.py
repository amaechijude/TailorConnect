# from django.shortcuts import render
# from django.http.response import JsonResponse

# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework_simplejwt.tokens import RefreshToken

# # from .serializer import UserSerializer, LoginSerializer
# # Create your views here.

# def get_token_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         "refresh_token": str(refresh),
#         "access_token": str(refresh.access_token)
#     }


# @api_view(['POST'])
# def register(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token = get_token_for_user(user)
#             output = {
#                 "Message": "Registration successfull", 

#                 "data": {
#                     "userId": user.userId,
#                     "email": user.email,
#                     },
#                 "token": {
#                     "refresh_token": token["refresh_token"],
#                     "access_token": token["access_token"],
#                 },
#             }
#             return Response(output, status.HTTP_201_CREATED)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def login_user(request):
#     serializer = LoginSerializer(data=request.data,context={"request":request})
#     if serializer.is_valid():
#         user = serializer.validated_data['user']
#         token = get_token_for_user(user)
#         user_output = {
#                 "message": "Login Succesfull",
#                 "data": {
#                     "userId": user.userId,
#                     "email": user.email,
#                     },
#                 "tokens":{
#                     "refresh_token":token['refresh_token'],
#                     "access_token": token['access_token'],
#                     },
#                 }
#         return Response(user_output, status.HTTP_200_OK)
#     return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)


# @api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
# def logout_user(request):
    
#     return Response({"success": "Token Worked"}, status.HTTP_200_OK)

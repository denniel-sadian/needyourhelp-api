from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.middleware.csrf import get_token
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer


class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({
                    "token": user.auth_token.key,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def log_out(request):
    logout(request)
    return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def me(request):
    if request.user.is_authenticated:
        return Response(data=UserSerializer(request.user).data,
                        status=status.HTTP_200_OK)
    return Response(data={}, status=status.HTTP_200_OK)
    

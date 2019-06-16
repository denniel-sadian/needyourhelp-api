from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.middleware.csrf import get_token
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from .serializers import PasswordSerializer
from .serializers import LoginSerializer


class CreateUserView(CreateAPIView):
    """
    View for creating users.
    """
    serializer_class = UserSerializer


class LoginView(GenericAPIView):
    """
    View for logging user in.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(username=data['username'],
                            password=data['password'])
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


class MeView(RetrieveUpdateAPIView):
    """
    View for retrieving and updating user instance.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    """
    View for changing password.
    """
    serializer_class = PasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
    
    def update(self, request):
        """Update the password."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        
        auth = authenticate(username=user.username,
                            password=serializer.data['password'])
        if auth is None:
            return Response({'detail': 'Wrong password.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.data['password2'])
        user.save()
        
        return Response({'detail': 'Password has been changed.'},
                        status=status.HTTP_200_OK)


@api_view(['GET'])
def log_out(request):
    """
    For logging out the user.
    """
    logout(request)
    return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)

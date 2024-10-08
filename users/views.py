import django.contrib.auth.password_validation as validators
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.views import APIView
from ShopZoneConfig.utils import CustomResponse
from .models import *
from .filters import *
from .serializers import *


class LoginView(GenericAPIView):
    """Login view for accessing the app"""
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            self.serializer = self.get_serializer(data=request.data)
            self.serializer.is_valid(raise_exception=True)
            # generate a token for that user, and login
            self.user = self.serializer.validated_data['user']
            refresh = RefreshToken.for_user(self.user)
            login(request, self.user)
            # get the user details of the logged in user
            user_info = UserSerializer(self.user).data if self.user else []
            return Response({
                "success": True,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "data": user_info,
                "message": "Login successful",
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return CustomResponse.failed(message="Invalid login credentials")


class SignupView(GenericAPIView):
    """User Signup View"""
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                self.serializer = self.get_serializer(data=request.data)
                self.serializer.is_valid(raise_exception=True)

                email = self.serializer.validated_data.get('email').lower()
                # check if a user with the email exists
                if User.objects.filter(email=email).exists():
                    raise Exception("A user with this email address already exists")

                # check if a user with the username exists
                username = self.serializer.validated_data.get('username').lower()
                if User.objects.filter(username=username).exists():
                    raise Exception("A user with this username already exists")

                # create the user account
                password = self.serializer.validated_data.get('password')
                user_type = self.serializer.validated_data.get('user_type')
                user = User.objects.create_user(email=email, password=password, 
                    user_type=user_type, username=username)
                user_info = UserSerializer(user).data
                return CustomResponse.success(data=user_info, message="Registration successful",
                    status=status.HTTP_201_CREATED)
        except Exception as e:
            return CustomResponse.failed(message=str(e))


class TokenRefreshView(GenericAPIView):
    """A view to refresh the access token, by using the refresh token"""
    serializer_class = TokenRefreshSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            self.serializer = self.get_serializer_class()
            self.serializer = self.serializer(data=request.data)
            self.serializer.is_valid(raise_exception=True)
            access_token = self.serializer.save()
            return CustomResponse.success(data=access_token, message="Token refresh successful")
        except Exception as e:
            return CustomResponse.failed(message="Token refresh unsuccessful")


class LogoutView(APIView):
    """View to logout the user"""
    def post(self, request, *args, **kwargs):
        logout(request)
        return CustomResponse.success(message="Logout successful")


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def get_queryset(self):
        query = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            return query if user.user_type == "admin" or user.is_superuser else query.filter(id=user.id)
        return query.none()


from django.core import validators
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(style={"input_type": 'password'})

    def validate(self, data):
        email = data.get('email').lower()
        password =  data.get('password')
        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                data['user'] = user
            else: raise serializers.ValidationError('Invalid email or password')
        else: raise serializers.ValidationError('Enter your email and password')
        return data


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=500, required=True)

    def create(self, validated_data):
        refresh = validated_data.get('refresh_token')
        try:
            # generate a new access token using the refresh token
            refresh_token = RefreshToken(refresh)
            access_token = str(refresh_token.access_token)
            return access_token
        except Exception as e: raise Exception(str(e))


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(max_length=255, required=True)
    user_type = serializers.CharField(max_length=5, required=False)
    password = serializers.CharField(style={"input_type": 'password'})

    def validate(self, data):
        password = data.get('password')
        try:
            validators.validate_password(password=password)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return super().validate(data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['date_joined', 'groups', 'user_permissions', 'last_login', 'is_active', 'is_superuser']


class ShopZoneUserSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    def get_euser_info(self, obj):
        # returns the user_info
        info = {
            "first_name" : obj.owner.first_name,
            "last_name" : obj.owner.last_name,
            "email_address" : obj.owner.email_address,
        }
        return info

    class Meta:
        model = ShopZoneUser
        fields = '__all__'

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


class UserProfileManager(BaseUserManager):
    def create_user(self, email=None, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required.")
        if not username:
            raise ValueError("The Username field is required.")

        # Normalize the email and username
        email = self.normalize_email(email.lower())
        username = username.lower()

        # Create the user with email, username, and password
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required.")
        if not username:
            raise ValueError("The Username field is required.")
        if not password:
            raise ValueError("The password field is required.")

        # Normalize the email
        email = self.normalize_email(email.lower())

        # Create the superuser
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )
        user.is_superuser = user.is_staff = user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    user_type_options = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField('User Type', choices=user_type_options, max_length=255, default='user')
    username = models.CharField('username', unique=True, db_index=True)
    email = models.EmailField('email address', unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserProfileManager()

    USERNAME_FIELD = 'username'  # Make sure username is used as the primary identifier
    REQUIRED_FIELDS = ['email']  # Email is now a required field when creating a superuser

    class Meta:
        ordering = ('-id',)


import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


class UserProfileManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Kindly enter an email address for this user.")

        # create the user, using the given email and password
        user = self.model(
            email=self.normalize_email(email.lower()),
            username=self.normalize_email(email.lower()),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        if password is None:
            raise ValueError("Kindly enter a valid password for this superuser.")

        # create the superuser, using the given email and password
        user = self.create_user(email, password)
        user.is_superuser, user.is_staff = True, True
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class ShopZoneUser(models.Model):
    user_type_options= (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    user_type = models.CharField('User Type', choices=user_type_options, max_length=255, default='user')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


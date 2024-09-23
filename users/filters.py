from django_filters import rest_framework as filters
from .models import *


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['id', 'email', 'user_type', 'username']


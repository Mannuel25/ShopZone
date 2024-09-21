from django_filters import rest_framework as filters
from .models import *


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['id', 'email']



class ShopZoneUserFilter(filters.FilterSet):
    class Meta:
        model = ShopZoneUser
        fields = ['owner', 'username', 'user_type']


from django_filters import rest_framework as filters
from .models import *


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name']


class StoreFilter(filters.FilterSet):
    class Meta:
        model = Store
        fields = ['owner', 'name']


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = '__all__'



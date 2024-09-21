from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db import transaction
from rest_framework import serializers, exceptions
from .models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    owner_details = serializers.SerializerMethodField(read_only=True)

    def get_owner_details(self, obj):
        # return the details of the store owner
        try:
            return {
                "username" : obj.owner.username,
                "email" : obj.owner.email,
            }
        except: return {}


    class Meta:
        model = Store
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_store(self, obj):
        # return the store details
        try: return StoreSerializer(obj.store).data
        except: return {}

    def get_category(self, obj):
        # return the category details
        try: return CategorySerializer(obj.category).data
        except: return {}


    class Meta:
        model = Product
        fields = '__all__'


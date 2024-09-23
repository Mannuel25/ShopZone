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
    store_details = serializers.SerializerMethodField(read_only=True)
    category_details = serializers.SerializerMethodField(read_only=True)
    converted_price = serializers.SerializerMethodField()

    def get_converted_price(self, obj):
        return getattr(obj, 'converted_price', obj.price)

    def get_store_details(self, obj):
        # returns the store details
        try:
            data = {
                "owner_details" : {
                    "email" : obj.store.owner.email,
                    "username" : obj.store.owner.username
                },
                "name" : obj.store.name,
                "description" : obj.store.description,
                "address" : obj.store.address
            }
            return data
        except: return {}

    def get_category_details(self, obj):
        # returns the category details
        try:
            data = {
                "name" : obj.category.name,
                "description" : obj.category.description,
            }
            return data
        except: return {}

    class Meta:
        model = Product
        fields = '__all__'


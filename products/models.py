from django.db import models
from users.models import ShopZoneUser
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    description = models.CharField(max_length=255, unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    owner = models.ForeignKey(ShopZoneUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    description = models.CharField(max_length=255, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    description = models.CharField(max_length=255, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    quantity = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


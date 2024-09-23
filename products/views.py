from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils.cache import get_cache_key
from .models import *
from .filters import *
from .serializers import *
from ShopZoneConfig.permissions import *
from ShopZoneConfig.common import CachedModelViewSet
from rest_framework.viewsets import ModelViewSet

class CategoryViewSet(CachedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filterset_class = CategoryFilter


class StoreViewSet(CachedModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filterset_class = StoreFilter


class ProductViewSet(CachedModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filterset_class = ProductFilter


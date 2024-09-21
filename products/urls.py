from django.urls import re_path as url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

app_name = "product_mgt"

router.register('categories', CategoryViewSet, basename='categories')
router.register('stores', StoreViewSet, basename='stores')
router.register('products', ProductViewSet, basename='products')


urlpatterns = [
    url(r'', include(router.urls)),
]


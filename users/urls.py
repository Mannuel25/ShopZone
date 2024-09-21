from django.urls import re_path as url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

app_name = "user_mgt"

router.register('users', ShopZoneUsersViewSet, basename='users')
router.register('app_users', UserViewSet, basename='app_users')


urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
]
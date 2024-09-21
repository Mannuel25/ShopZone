from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view as gs
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings

schema_view = gs(
    openapi.Info(
        title="ShopZone API",
        default_version='1.0.0',
        description="Documentation for ShopZone API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="oluwasegunprosperity@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('shopzone-admin/', admin.site.urls),
    path('api/user_mgt/', include('users.urls')),
    path('api/product_mgt/', include('products.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

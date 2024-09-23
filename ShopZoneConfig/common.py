from rest_framework.viewsets import ModelViewSet
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils.cache import get_cache_key


class CachedModelViewSet(ModelViewSet):
    cache_timeout = 60 * 5

    @method_decorator(cache_page(cache_timeout))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(cache_timeout))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        response = super().perform_create(serializer)
        self.invalidate_cache(serializer.instance)
        return response

    def perform_update(self, serializer):
        response = super().perform_update(serializer)
        self.invalidate_cache(serializer.instance)
        return response

    def perform_destroy(self, instance):
        response = super().perform_destroy(instance)
        self.invalidate_cache(instance)
        return response

    def invalidate_cache(self, instance):
        cache_key_list = get_cache_key(self.request, self.request.resolver_match)
        print('cache_key_list:', cache_key_list)
        cache_key_detail = f"{cache_key_list}_{instance.pk}"
        print('cache_key_detail:', cache_key_detail)
        if cache_key_list:
            cache.delete(cache_key_list)
        if cache_key_detail:
            cache.delete(cache_key_detail)


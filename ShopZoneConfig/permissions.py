from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission, SAFE_METHODS
from products.models import Store, Product


class IsAdmin(BasePermission):
    """
    Custom permission to only allow admins to edit, update, or delete objects.
    """

    def has_permission(self, request, view):
        return request.user.user_type == 'admin'


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow users to view any product/store, 
    but only owners or admins can edit or delete.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # admins can edit or delete any product/store
        if request.user.user_type == 'admin':
            return True

        # allow only the store owner to edit or delete
        if isinstance(obj, Store):
            return obj.owner == request.user and request.method in ['PUT', 'PATCH', 'DELETE']

        # allow only the owner of the store associated with the product to edit or delete
        if isinstance(obj, Product):
            return obj.store.owner == request.user and request.method in ['PUT', 'PATCH', 'DELETE']

        return False

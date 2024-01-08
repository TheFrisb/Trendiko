from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsStockManager(BasePermission):
    def has_permission(self, request, view):
        has_permission = request.user.groups.filter(name="stock_manager").exists()
        if not has_permission:
            raise PermissionDenied(detail="You must be a stock manager to access this.")
        return True

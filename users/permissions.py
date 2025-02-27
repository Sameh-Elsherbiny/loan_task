from rest_framework.permissions import BasePermission
from .models import CustomUser

class ProviderPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.user_type == 'LP'
        return False
    
class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.user_type == 'LC'
        return False
    
class BankPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.user_type == 'BK'
        return False
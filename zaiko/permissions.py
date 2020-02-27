from rest_framework import permissions

from zaiko import constant
from users.models import UserRole


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # check if valid token has been provided
        try:
            return request.user.is_authenticated
        except AttributeError:
            return False


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        # check if user have admin role
        try:
            user_role = UserRole.objects.get(name=constant.ROLE_ADMIN)
            return user_role.id == request.user.user_role_id
        except UserRole.DoesNotExist:
            return False


class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        # check if user have admin role
        try:
            user_role = UserRole.objects.get(name=constant.ROLE_CUSTOMER)
            return user_role.id == request.user.user_role_id
        except UserRole.DoesNotExist:
            return False


class IsMerchant(permissions.BasePermission):

    def has_permission(self, request, view):
        # check if user have admin role
        try:
            user_role = UserRole.objects.get(name=constant.ROLE_MERCHANT)
            return user_role.id == request.user.user_role_id
        except UserRole.DoesNotExist:
            return False

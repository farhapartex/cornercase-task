from rest_framework.permissions import BasePermission
from user.enums import RoleChoices


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleChoices.ADMIN.value


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleChoices.OWNER.value


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleChoices.EMPLOYEE.value


from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class IsAccountExecutive(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        is_authenticated = request.user.is_authenticated
        has_role_attr = hasattr(request.user, "role")
        user_role = request.user.role == "account_executive"

        return is_authenticated and has_role_attr and user_role


class IsTeller(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        is_authenticated = request.user.is_authenticated
        has_role_attr = hasattr(request.user, "role")
        user_role = request.user.role == "teller"

        return is_authenticated and has_role_attr and user_role


class IsBranchManager(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        is_authenticated = request.user.is_authenticated
        has_role_attr = hasattr(request.user, "role")
        user_role = request.user.role == "branch_manager"

        return is_authenticated and has_role_attr and user_role

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsAdmin(BasePermission):
    """
    Пользователь является супрюзером джанго
    или имеет роль администратора.
    """
    def has_permission(self, request, view):
        return (request.user.role == User.ADMIN_ROLE
                or request.user.is_superuser)


class IsSelf(BasePermission):
    """Пользователь делает запрос о своём аккаунте."""
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return get_object_or_404(
            User,
            username=request.data.get('username'),
            email=request.data.get('email')
        ) == request.user

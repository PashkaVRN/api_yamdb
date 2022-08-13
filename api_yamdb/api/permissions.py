from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsAuthorOrReadOnly(BasePermission):
    """
    Позволяет редактировать объекты только их автору.
    Для остальных пользователей объекты доступны только для чтения.
    """
    def has_object_permission(self, request, view, obj):
        return True if (
            request.method in SAFE_METHODS
        ) else obj.author == request.user


class IsAdmin(BasePermission):
    """
    Пользователь является супрюзером джанго
    или имеет роль администратора.
    """
    def has_permission(self, request, view):
        user = request.user
        if request.user.is_authenticated:
            return (
                user.is_authenticated
                and (request.user.role == User.ADMIN_ROLE
                     or request.user.is_superuser)
            )


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


class IsAdminOrReadOnly(BasePermission):
    """
    Пользователь является супрюзером джанго
    или имеет роль администратора.
    Просмотр доступен всем пользователям.
    """
    def has_permission(self, request, view):
        user = request.user
        return True if (

            request.method in SAFE_METHODS) else (
                user.is_authenticated
                and (user.role == User.ADMIN_ROLE
                     or user.is_superuser))


class IsModeratorAdminOrReadOnly(BasePermission):
    """
    Пользователь является супрюзером джанго
    или имеет роль администратора или модератора.
    Просмотр доступен всем пользователям.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.ADMIN_ROLE
            or request.user.role == User.MODERATOR_ROLE
            or request.user.is_superuser)

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

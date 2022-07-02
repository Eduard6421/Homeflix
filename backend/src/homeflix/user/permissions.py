
from rest_framework import permissions


class UserViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.action == 'list' or view.action == 'retrieve'


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser

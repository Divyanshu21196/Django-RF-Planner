from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access certain views.
    """

    message="Only superusers are allowed to perform this action."

    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated and request.user.is_super_user


class IsOwnerOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or superusers to access it.
    """

    message="You must be the owner of this object or a superuser to perform this action."

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user or request.user.is_super_user


class IsOwnerReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it, but allow read-only access to others.
    """

    message="You can only modify your own information."

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return hasattr(obj, 'created_by') and obj.created_by == request.user
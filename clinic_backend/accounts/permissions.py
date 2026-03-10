from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'DOCTOR'

class IsAdminOrReadOnly(BasePermission):
    """
    Allow read access to all authenticated users, but write access only to admins.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.method == 'GET':
                return True
            return request.user.role == 'ADMIN'
        return False

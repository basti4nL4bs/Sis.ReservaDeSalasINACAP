from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso granular: solo el usuario dueño de la reserva o personal staff
    pueden ver en detalle, actualizar o eliminar la reserva.
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj.usuario == request.user


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Permite métodos de solo lectura (GET, HEAD, OPTIONS) a cualquier usuario.
    Las mutaciones (POST, PUT, PATCH, DELETE) requieren privilegios de staff.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
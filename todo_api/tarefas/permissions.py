from rest_framework.permissions import BasePermission

class EhDono(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user
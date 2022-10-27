from rest_framework.permissions import BasePermission


class perm_for_shop(BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 'shop':
            return True
        return f'Error! Only for shops.'

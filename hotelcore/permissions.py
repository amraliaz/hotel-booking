from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # ادمین همیشه دسترسی داره
        if request.user.is_staff:
            return True

        # فقط صاحب رزرو دسترسی داره
        return obj.user == request.user
from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from users.models import RolePermission


class RoleModelPermission(permissions.BasePermission):
    def _get_model_from_view(self, view):
        if hasattr(view, 'model'):
            return view.model
        queryset = getattr(view, 'queryset', None)
        if queryset is not None:
            return queryset.model
        get_qs = getattr(view, 'get_queryset', None)
        if get_qs:
            try:
                return get_qs().model
            except Exception:
                return None
        return None

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if not getattr(user, 'role_id', None):
            return False

        model = self._get_model_from_view(view)
        if model is None:
            return False

        ct = ContentType.objects.get_for_model(model)
        try:
            rp = RolePermission.objects.get(role=user.role_id, content_type=ct)
        except RolePermission.DoesNotExist:
            return False

        if request.method in permissions.SAFE_METHODS:
            return rp.can_view
        if request.method == "POST":
            return rp.can_create
        if request.method in ("PUT", "PATCH"):
            return rp.can_edit
        if request.method == "DELETE":
            return rp.can_delete

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

from django.contrib import admin
from .models import CustomUser, Role, RolePermission

# Register your models here.
class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1
    autocomplete_fields = ['content_type']
    fields = ('content_type', 'can_view', 'can_create', 'can_edit', 'can_delete')

    
admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(RolePermission)
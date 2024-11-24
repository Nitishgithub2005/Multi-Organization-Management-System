from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Organization, CustomUser, Role

# Resources for Import-Export
class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'organization__name', 'role__name', 'is_staff', 'is_superuser')
        export_order = ('id', 'username', 'email', 'organization__name', 'role__name', 'is_staff', 'is_superuser')

class OrganizationResource(resources.ModelResource):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'address', 'is_main')
        export_order = ('id', 'name', 'address', 'is_main')

class RoleResource(resources.ModelResource):
    class Meta:
        model = Role
        fields = ('id', 'name')
        export_order = ('id', 'name')

# Admins with Import-Export Functionality
class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    resource_class = CustomUserResource
    list_display = ('username', 'email', 'organization', 'role', 'is_staff')
    list_filter = ('organization', 'role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Organization Info', {'fields': ('organization', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Organization Info', {'fields': ('organization', 'role')}),
    )

@admin.register(Organization)
class OrganizationAdmin(ImportExportModelAdmin):
    resource_class = OrganizationResource
    list_display = ('name', 'address', 'is_main')
    list_filter = ('is_main',)

@admin.register(Role)
class RoleAdmin(ImportExportModelAdmin):
    resource_class = RoleResource
    list_display = ('name',)

# Register CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
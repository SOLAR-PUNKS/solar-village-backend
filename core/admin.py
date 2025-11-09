from django.contrib import admin
from .models import MutualAidPost, User, CommunityResource

try:
    from django.contrib.gis.admin import OSMGeoAdmin
    GeoAdminBase = OSMGeoAdmin
except ImportError:
    # Fallback if GIS is not available (e.g., GDAL not installed)
    GeoAdminBase = admin.ModelAdmin


@admin.register(MutualAidPost)
class MutualAidPostAdmin(GeoAdminBase):
    list_display = ['title', 'type', 'category', 'status', 'created_by', 'created_at']
    list_filter = ['type', 'category', 'status', 'created_at']
    search_fields = ['title', 'description', 'address', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('type', 'title', 'description', 'category', 'status')
        }),
        ('Location', {
            'fields': ('location', 'address')
        }),
        ('Contact', {
            'fields': ('contact_info',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityResource)
class CommunityResourceAdmin(GeoAdminBase):
    list_display = ['name', 'resource_type', 'city', 'state', 'is_active', 'created_at']
    list_filter = ['resource_type', 'is_active', 'state', 'city', 'created_at']
    search_fields = ['name', 'description', 'address', 'city', 'state']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('resource_type', 'name', 'description', 'is_active')
        }),
        ('Location', {
            'fields': ('location', 'address', 'city', 'state', 'zip_code')
        }),
        ('Contact', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Details', {
            'fields': ('hours', 'eligibility_requirements', 'services')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

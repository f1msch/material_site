from django.contrib import admin
from .models import Category, Tag, Material, Favorite, DownloadHistory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'sort_order', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'material_type', 'status', 'view_count', 'download_count', 'created_at']
    list_filter = ['status', 'material_type', 'license_type', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['view_count', 'download_count', 'like_count', 'favorite_count']
    filter_horizontal = ['tags']
    fieldsets = (
        ('基础信息', {
            'fields': ('title', 'slug', 'description', 'material_type', 'author')
        }),
        ('分类和标签', {
            'fields': ('category', 'tags')
        }),
        ('文件信息', {
            'fields': ('main_file', 'thumbnail', 'preview_image')
        }),
        ('元数据', {
            'fields': ('file_size', 'dimensions', 'duration')
        }),
        ('权限和状态', {
            'fields': ('license_type', 'price', 'status', 'is_featured')
        }),
        ('统计信息', {
            'fields': ('view_count', 'download_count', 'like_count', 'favorite_count')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'published_at')
        }),
    )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'material', 'created_at']
    list_filter = ['created_at']

@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'material', 'downloaded_at', 'ip_address']
    list_filter = ['downloaded_at']
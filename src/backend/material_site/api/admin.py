from django.contrib import admin
from .models import Category, Material, MaterialTag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'material_type', 'price', 'is_free', 'downloads', 'created_at']
    list_filter = ['category', 'material_type', 'is_free']
    search_fields = ['title']

admin.site.register(MaterialTag)
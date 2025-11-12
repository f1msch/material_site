from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'material_site', views.MaterialViewSet, basename='material')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'favorites', views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]
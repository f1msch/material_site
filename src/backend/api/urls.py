from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'materials', views.MaterialViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
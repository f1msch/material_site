
# blog/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PostViewSet, CommentListAPIView, CategoryListAPIView

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentListAPIView.as_view(), name='post-comments'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
]

# 在主urls.py中添加
urlpatterns += [
    path('api/', include('blog.api_urls')),
]
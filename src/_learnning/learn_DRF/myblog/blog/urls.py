# blog/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PostViewSet, CommentListAPIView, CategoryListAPIView, approve_comment

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentListAPIView.as_view(), name='post-comments'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('comments/<int:comment_id>/approve/', approve_comment, name='approve-comment'),
]
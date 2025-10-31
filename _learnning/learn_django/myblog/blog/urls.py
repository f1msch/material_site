# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
]

# blog/permissions.py
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只允许作者编辑自己的文章
    """

    def has_object_permission(self, request, view, obj):
        # 读取权限允许所有请求
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限只允许作者
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只允许管理员用户编辑
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# 在视图中使用
class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
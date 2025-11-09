from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from .models import Material, Category, Tag, Favorite, DownloadHistory
from .serializers import *
from .filters import MaterialFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class MaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MaterialFilter
    search_fields = ['title', 'description', 'tags__name']
    ordering_fields = ['created_at', 'view_count', 'download_count', 'like_count', 'price']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Material.objects.filter(status='approved').select_related(
            'author', 'category'
        ).prefetch_related('tags')

        if self.request.user.is_authenticated and self.action in ['my_materials', 'drafts']:
            return Material.objects.filter(author=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return MaterialCreateSerializer
        elif self.action == 'list':
            return MaterialListSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return MaterialDetailSerializer
        return MaterialListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def my_materials(self, request):
        """获取当前用户的素材"""
        queryset = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'])
    def drafts(self, request):
        """获取当前用户的草稿"""
        queryset = Material.objects.filter(author=request.user, status='draft')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """收藏/取消收藏素材"""
        material = self.get_object()
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            material=material
        )

        if not created:
            favorite.delete()
            material.favorite_count -= 1
            is_favorited = False
        else:
            material.favorite_count += 1
            is_favorited = True

        material.save()
        return Response({'favorited': is_favorited, 'count': material.favorite_count})

    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """下载素材"""
        material = self.get_object()

        # 记录下载历史
        DownloadHistory.objects.create(
            user=request.user,
            material=material,
            ip_address=self.get_client_ip(request)
        )

        # 更新下载计数
        material.download_count += 1
        material.save()

        # 更新用户的下载统计
        request.user.downloads_count += 1
        request.user.save()

        return Response({
            'download_url': material.main_file.url,
            'download_count': material.download_count
        })

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞素材"""
        material = self.get_object()
        material.like_count += 1
        material.save()
        return Response({'like_count': material.like_count})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('material')

    def perform_create(self, serializer):
        material_id = self.request.data.get('material')
        material = get_object_or_404(Material, id=material_id)
        serializer.save(user=self.request.user, material=material)
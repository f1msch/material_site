"""
素材视图模块
处理所有与素材相关的API请求
"""

import logging
from typing import Optional
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from .filters import MaterialFilter
from .models import Material, Category, Tag, Favorite, DownloadHistory
from .serializers import (
    CategorySerializer, TagSerializer, MaterialListSerializer,
    MaterialDetailSerializer, MaterialCreateSerializer, FavoriteSerializer
)
from src.backend.exceptions import (
    ValidationError, NotFoundError, MaterialUploadError
)

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    分类视图集
    处理分类相关的只读操作
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    标签视图集
    处理标签相关的只读操作
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class MaterialViewSet(viewsets.ModelViewSet):
    """
    素材视图集
    处理素材的CRUD操作和其他业务逻辑

    Attributes:
        permission_classes: 权限控制类
        filter_backends: 过滤器后端
        filterset_class: 过滤器类
        search_fields: 搜索字段
        ordering_fields: 排序字段
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MaterialFilter
    search_fields = ['title', 'description', 'tags__name']
    ordering_fields = ['created_at', 'view_count', 'download_count', 'like_count', 'price']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        获取查询集

        Returns:
            QuerySet: 根据用户权限过滤的查询集
        """
        queryset = Material.objects.filter(status='approved').select_related(
            'author', 'category'
        ).prefetch_related('tags')

        # 用户查看自己的素材或草稿
        if self.request.user.is_authenticated and self.action in ['my_materials', 'drafts']:
            return Material.objects.filter(author=self.request.user)

        return queryset

    def get_serializer_class(self):
        """
        根据action获取对应的序列化器类

        Returns:
            Serializer class: 序列化器类
        """
        action_serializer_map = {
            'create': MaterialCreateSerializer,
            'list': MaterialListSerializer,
            'retrieve': MaterialDetailSerializer,
            'update': MaterialDetailSerializer,
            'partial_update': MaterialDetailSerializer,
        }
        return action_serializer_map.get(self.action, MaterialListSerializer)

    def perform_create(self, serializer):
        """
        执行创建操作

        Args:
            serializer: 序列化器实例
        """
        try:
            serializer.save(author=self.request.user)
            logger.info(f"User {self.request.user.id} created material")
        except Exception as e:
            logger.error(f"Failed to create material: {str(e)}")
            raise MaterialUploadError(f"上传素材失败: {str(e)}")

    @action(detail=False, methods=['get'])
    def my_materials(self, request: Request) -> Response:
        """
        获取当前用户的素材

        Args:
            request: HTTP请求

        Returns:
            Response: 分页响应
        """
        try:
            queryset = self.get_queryset().filter(author=request.user)
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error(f"Failed to get user materials: {str(e)}")
            raise ValidationError("获取用户素材失败")

    @action(detail=False, methods=['get'])
    def drafts(self, request: Request) -> Response:
        """获取当前用户的草稿"""
        try:
            queryset = Material.objects.filter(author=request.user, status='draft')
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error(f"Failed to get drafts: {str(e)}")
            raise ValidationError("获取草稿失败")

    @action(detail=True, methods=['post'])
    def favorite(self, request: Request, pk: Optional[int] = None) -> Response:
        """
        收藏/取消收藏素材

        Args:
            request: HTTP请求
            pk: 素材ID

        Returns:
            Response: 收藏状态和计数
        """
        try:
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

            return Response({
                'favorited': is_favorited,
                'count': material.favorite_count
            })

        except Material.DoesNotExist:
            raise NotFoundError("素材不存在")
        except Exception as e:
            logger.error(f"Favorite operation failed: {str(e)}")
            raise ValidationError("收藏操作失败")

    @action(detail=True, methods=['post'])
    def download(self, request: Request, pk: Optional[int] = None) -> Response:
        """
        下载素材

        Args:
            request: HTTP请求
            pk: 素材ID

        Returns:
            Response: 下载URL和统计信息
        """
        try:
            material = self.get_object()

            if not material.main_file:
                raise ValidationError("素材文件不存在")

            # 记录下载历史
            DownloadHistory.objects.create(
                user=request.user,
                material=material,
                ip_address=self.get_client_ip(request)
            )

            # 更新统计
            material.download_count += 1
            material.save()

            # 更新用户统计
            request.user.downloads_count += 1
            request.user.save()

            logger.info(f"User {request.user.id} downloaded material {material.id}")

            return Response({
                'download_url': material.main_file.url,
                'download_count': material.download_count
            })

        except Material.DoesNotExist:
            raise NotFoundError("素材不存在")
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            raise ValidationError(f"下载失败: {str(e)}")

    @action(detail=True, methods=['post'])
    def like(self, request: Request, pk: Optional[int] = None) -> Response:
        """点赞素材"""
        try:
            material = self.get_object()
            material.like_count += 1
            material.save()

            return Response({'like_count': material.like_count})

        except Material.DoesNotExist:
            raise NotFoundError("素材不存在")
        except Exception as e:
            logger.error(f"Like operation failed: {str(e)}")
            raise ValidationError("点赞失败")

    @staticmethod
    def get_client_ip(request: Request) -> Optional[str]:
        """
        获取客户端IP地址

        Args:
            request: HTTP请求

        Returns:
            str: IP地址
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class FavoriteViewSet(viewsets.ModelViewSet):
    """收藏视图集"""
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """获取当前用户的收藏"""
        return Favorite.objects.filter(user=self.request.user).select_related('material')

    def perform_create(self, serializer):
        """创建收藏记录"""
        material_id = self.request.data.get('material')
        if not material_id:
            raise ValidationError("需要提供素材ID")

        material = get_object_or_404(Material, id=material_id)
        serializer.save(user=self.request.user, material=material)
import os
from django.db.models import Q
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.response import Response

from .models import Material, Category
from .models import Material, Category
from .serializers import MaterialListSerializer, MaterialDetailSerializer, CategorySerializer
from .serializers import MaterialSerializer, CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

#
# class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Material.objects.all()
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['category', 'material_type', 'is_free']
#     search_fields = ['title', 'description', 'tags__name']
#     ordering_fields = ['created_at', 'downloads', 'likes', 'price']
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return MaterialDetailSerializer
#         return MaterialListSerializer
#
#     @action(detail=True, methods=['post'])
#     def download(self, request, pk=None):
#         material = self.get_object()
#         material.downloads += 1
#         material.save()
#         return Response({'downloads': material.downloads})
#
#     @action(detail=True, methods=['post'])
#     def like(self, request, pk=None):
#         material = self.get_object()
#         material.likes += 1
#         material.save()
#         return Response({'likes': material.likes})
#

from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all().select_related('category').order_by('-created_at')
    serializer_class = MaterialSerializer
    pagination_class = StandardPagination

    def create(self, request, *args, **kwargs):
        """处理素材上传"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # 保存素材，这会自动触发缩略图生成
                material = serializer.save()

                # 返回创建的数据
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'error': f'上传失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_queryset(self):
        """根据查询参数过滤素材"""
        queryset = super().get_queryset()

        # 按类型过滤
        material_type = self.request.query_params.get('type')
        if material_type:
            queryset = queryset.filter(material_type=material_type)

        # 按分类过滤
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset

    @action(detail=True, methods=['get'])
    def download_file(self, request, pk=None):
        """下载素材文件"""
        material = self.get_object()

        # 增加下载计数
        material.downloads += 1
        material.save(update_fields=['downloads'])

        if material.file:
            response = HttpResponse(
                material.file.read(),
                content_type='application/octet-stream'
            )
            filename = os.path.basename(material.file.name)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        return Response({'error': '文件不存在'}, status=404)

    @action(detail=True, methods=['get'])
    def download_thumbnail(self, request, pk=None):
        """下载缩略图"""
        material = self.get_object()

        if material.thumbnail:
            response = HttpResponse(
                material.thumbnail.read(),
                content_type='image/jpeg'
            )
            filename = os.path.basename(material.thumbnail.name)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        return Response({'error': '缩略图不存在'}, status=404)

    @action(detail=True, methods=['get'])
    def preview_image(self, request, pk=None):
        """预览图片（原图）"""
        material = self.get_object()

        if material.material_type == 'image' and material.file:
            response = HttpResponse(
                material.file.read(),
                content_type='image/jpeg'
            )
            response['Content-Disposition'] = 'inline'
            return response

        return Response({'error': '不是图片文件或文件不存在'}, status=404)

    @action(detail=False, methods=['get'])
    def image_materials(self, request):
        """获取所有图片类型的素材"""
        images = self.get_queryset().filter(material_type='image')
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """创建素材，处理文件上传"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 保存素材
            material = serializer.save()

            # 如果是图片，确保处理图片信息
            if material.material_type == 'image' and material.file:
                material.process_image_file()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
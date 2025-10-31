from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Material, Category
from .serializers import MaterialListSerializer, MaterialDetailSerializer, CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'material_type', 'is_free']
    search_fields = ['title', 'description', 'tags__name']
    ordering_fields = ['created_at', 'downloads', 'likes', 'price']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MaterialDetailSerializer
        return MaterialListSerializer

    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        material = self.get_object()
        material.downloads += 1
        material.save()
        return Response({'downloads': material.downloads})

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        material = self.get_object()
        material.likes += 1
        material.save()
        return Response({'likes': material.likes})
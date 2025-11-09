from rest_framework import serializers

from .models import Material, Category, MaterialTag


class MaterialTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialTag
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class MaterialListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = MaterialTagSerializer(many=True, read_only=True)

    class Meta:
        model = Material
        fields = [
            'id', 'title', 'description', 'category', 'material_type',
            'image_preview', 'file_size', 'downloads', 'likes', 'price',
            'is_free', 'created_at', 'tags'
        ]


class MaterialSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    material_type_display = serializers.CharField(source='get_file_type_display', read_only=True)

    # 图片URL字段
    preview_url = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    # 图片信息
    image_info = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'material_type', 'material_type_display', 'file', 'file_size',
            'downloads', 'image_preview', 'image_width', 'image_height',
            'thumbnail', 'preview_url', 'file_url', 'thumbnail_url',
            'image_info', 'created_at', 'updated_at'
        ]
        read_only_fields = ['file_size', 'downloads', 'image_width', 'image_height', 'thumbnail']

    def get_preview_url(self, obj):
        if obj.image_preview:
            return obj.image_preview.url
        return None

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return None

    def get_image_info(self, obj):
        """获取图片详细信息"""
        if obj.material_type == 'image':
            return {
                'width': obj.image_width,
                'height': obj.image_height,
                'size': f"{obj.image_width} × {obj.image_height}",
                'file_size': self.format_file_size(obj.file_size)
            }
        return None

    def format_file_size(self, size_bytes):
        """格式化文件大小显示"""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.2f} {size_names[i]}"


class MaterialDetailSerializer(MaterialListSerializer):
    class Meta(MaterialListSerializer.Meta):
        fields = MaterialListSerializer.Meta.fields + ['file']
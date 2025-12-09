from rest_framework import serializers
from .models import Material, Category, Tag, Favorite
from users.serializers import UserSerializer
from src.backend.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    """
    分类序列化器
    用于分类数据的序列化和反序列化
    """
    material_count = serializers.IntegerField(source='materials.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'icon',
                  'sort_order', 'is_active', 'material_count', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'color', 'created_at']


class MaterialListSerializer(serializers.ModelSerializer):
    """
    素材列表序列化器
    用于素材列表展示，包含基本信息
    """
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    file_size_display = serializers.CharField(read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = [
            'id', 'title', 'slug', 'material_type', 'thumbnail', 'preview_image',
            'author', 'category', 'tags', 'view_count', 'download_count',
            'like_count', 'favorite_count', 'license_type', 'price',
            'file_size_display', 'dimensions', 'created_at', 'is_favorited'
        ]

    def get_is_favorited(self, obj: Material) -> bool:
        """
        获取当前用户是否收藏了该素材

        Args:
            obj: Material实例

        Returns:
            bool: 是否已收藏
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False


class MaterialDetailSerializer(MaterialListSerializer):
    """素材详情序列化器"""

    class Meta:
        model = Material
        fields = MaterialListSerializer.Meta.fields + [
            'description', 'main_file', 'duration', 'status',
            'is_featured', 'published_at', 'updated_at'
        ]


class MaterialCreateSerializer(serializers.ModelSerializer):
    """
    素材创建序列化器
    用于创建新素材，处理文件上传和标签
    """
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=[],
        write_only=True
    )

    class Meta:
        model = Material
        fields = [
            'title', 'description', 'material_type', 'category', 'tags',
            'main_file', 'thumbnail', 'preview_image', 'license_type', 'price'
        ]
        read_only_fields = ('author', 'slug', 'status', 'file_size')

    def validate_title(self, value: str) -> str:
        """验证标题"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("标题至少需要2个字符")
        if len(value) > 200:
            raise serializers.ValidationError("标题不能超过200个字符")
        return value.strip()

    def validate_tags(self, value: list) -> list:
        """
        验证标签数据

        Args:
            value: 标签列表

        Returns:
            list: 清理后的标签列表

        Raises:
            ValidationError: 标签格式错误
        """
        if not isinstance(value, list):
            raise ValidationError("标签必须是列表格式")

        cleaned_tags = []
        for tag_name in value:
            if tag_name and isinstance(tag_name, str) and tag_name.strip():
                cleaned_tag = tag_name.strip()[:30]  # 限制长度
                if cleaned_tag not in cleaned_tags:  # 去重
                    cleaned_tags.append(cleaned_tag)

        return cleaned_tags

    def validate_price(self, value: float) -> float:
        """验证价格"""
        if value < 0:
            raise serializers.ValidationError("价格不能为负数")
        if value > 1000000:  # 限制最大价格
            raise serializers.ValidationError("价格不能超过1,000,000")
        return round(value, 2)

    def create(self, validated_data: dict) -> Material:
        """
        创建素材记录

        Args:
            validated_data: 验证后的数据

        Returns:
            Material: 创建的素材实例
        """
        logger.info(f"Creating material with data: {validated_data.keys()}")

        try:
            # 1. 取出标签数据
            tags_data = validated_data.pop('tags', [])

            # 2. 创建素材记录
            material = Material.objects.create(**validated_data)
            logger.info(f"Material created: {material.id}")

            # 3. 处理标签
            if tags_data:
                tag_objects = []
                for tag_name in tags_data:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name.lower(),
                        defaults={'name': tag_name.lower()}
                    )
                    tag_objects.append(tag)

                # 建立多对多关联
                material.tags.set(tag_objects)
                logger.info(f"Tags associated: {len(tag_objects)} tags")

            return material

        except Exception as e:
            logger.error(f"Failed to create material: {str(e)}")
            raise ValidationError(f"创建素材失败: {str(e)}")

    def to_representation(self, instance: Material) -> dict:
        """
        序列化实例为字典

        Args:
            instance: Material实例

        Returns:
            dict: 序列化后的数据
        """
        data = super().to_representation(instance)
        data['tags'] = [tag.name for tag in instance.tags.all()]
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    material = MaterialListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'material', 'created_at']
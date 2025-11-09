from rest_framework import serializers
from .models import Material, Category, Tag, Favorite
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    material_count = serializers.IntegerField(source='materials.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'icon',
                  'sort_order', 'is_active', 'material_count', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'color', 'created_at']


class MaterialListSerializer(serializers.ModelSerializer):
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

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False


class MaterialDetailSerializer(MaterialListSerializer):
    class Meta:
        model = Material
        fields = MaterialListSerializer.Meta.fields + [
            'description', 'main_file', 'duration', 'status',
            'is_featured', 'published_at', 'updated_at'
        ]


class MaterialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            'title', 'description', 'material_type', 'category', 'tags',
            'main_file', 'thumbnail', 'preview_image', 'license_type', 'price'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        material = Material.objects.create(**validated_data)
        material.tags.set(tags)
        return material


class FavoriteSerializer(serializers.ModelSerializer):
    material = MaterialListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'material', 'created_at']
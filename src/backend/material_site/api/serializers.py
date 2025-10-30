from rest_framework import serializers
from materials.models import Material, Category, MaterialTag


class MaterialTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialTag
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


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


class MaterialDetailSerializer(MaterialListSerializer):
    class Meta(MaterialListSerializer.Meta):
        fields = MaterialListSerializer.Meta.fields + ['file']
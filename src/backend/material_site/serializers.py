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
    # 重写tags字段，接受字符串列表
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        default=[],
        write_only=True  # 只在创建时使用
    )

    class Meta:
        model = Material
        fields = [
            'title', 'description', 'material_type', 'category', 'tags',
            'main_file', 'thumbnail', 'preview_image', 'license_type', 'price'
        ]
        read_only_fields = ('author', 'slug', 'status', 'file_size')

    def validate_tags(self, value):
        """验证tags字段"""
        print("🔹 validate_tags 被调用")
        print("接收的tags:", value)

        if not isinstance(value, list):
            raise serializers.ValidationError("标签必须是列表格式")

        # 清理标签名称
        cleaned_tags = []
        for tag_name in value:
            if tag_name and isinstance(tag_name, str) and tag_name.strip():
                cleaned_tags.append(tag_name.strip())

        print("清理后的tags:", cleaned_tags)
        return cleaned_tags

    def create(self, validated_data):
        print("🔹 create 方法开始执行")

        # 1. 取出tags数据
        tags_data = validated_data.pop('tags', [])
        print("准备处理的tags数据:", tags_data)

        # 2. 创建素材记录（material表）
        print("创建Material记录...")
        material = Material.objects.create(**validated_data)
        print(f"✅ Material创建成功, ID: {material.id}")

        # 3. 处理标签（tags表 + 关联表）
        if tags_data:
            tag_objects = []
            for tag_name in tags_data:
                print(f"处理标签: '{tag_name}'")

                # 获取或创建标签（tags表）
                tag, created = Tag.objects.get_or_create(
                    name=tag_name.lower(),  # 统一小写存储
                    defaults={'name': tag_name.lower()}
                )
                tag_objects.append(tag)

                if created:
                    print(f"  ✅ 创建新标签: {tag.name} (ID: {tag.id})")
                else:
                    print(f"  🔹 使用现有标签: {tag.name} (ID: {tag.id})")

            # 建立多对多关联
            print("建立标签关联...")
            material.tags.set(tag_objects)
            print(f"✅ 关联完成: {material.title} ↔ {len(tag_objects)}个标签")
        else:
            print("⚠️ 没有标签数据")

        return material

    def to_representation(self, instance):
        """响应数据中显示标签名称"""
        data = super().to_representation(instance)
        data['tags'] = [tag.name for tag in instance.tags.all()]
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    material = MaterialListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'material', 'created_at']
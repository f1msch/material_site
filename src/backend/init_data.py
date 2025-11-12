import os
import django
from django.db import models
from django.utils import timezone
from datetime import timedelta

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from material_site.models import Category, Tag, Material
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

User = get_user_model()


def create_superuser():
    """创建超级用户"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@material.com',
            password='admin123',
            bio='系统管理员',
            website='https://material.com'
        )
        print("✅ 超级用户创建成功: admin / admin123")


def create_test_users():
    """创建测试用户"""
    users_data = [
        {
            'username': 'designer',
            'email': 'designer@material.com',
            'password': 'designer123',
            'bio': '专业平面设计师',
            'website': 'https://designer.com'
        },
        {
            'username': 'photographer',
            'email': 'photo@material.com',
            'password': 'photo123',
            'bio': '风景摄影师',
            'website': 'https://photo.com'
        },
        {
            'username': 'developer',
            'email': 'dev@material.com',
            'password': 'dev123',
            'bio': '前端开发者',
            'website': 'https://dev.com'
        }
    ]

    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                bio=user_data['bio'],
                website=user_data['website']
            )
            print(f"✅ 测试用户创建成功: {user_data['username']} / {user_data['password']}")


def create_categories():
    """创建分类数据"""
    categories_data = [
        {
            'name': '图片素材',
            'slug': 'images',
            'description': '高质量图片素材',
            'icon': '🖼️'
        },
        {
            'name': '矢量图形',
            'slug': 'vectors',
            'description': '可缩放矢量图形',
            'icon': '📐'
        },
        {
            'name': '视频素材',
            'slug': 'videos',
            'description': '高清视频素材',
            'icon': '🎬'
        },
        {
            'name': '音频素材',
            'slug': 'audio',
            'description': '音效和背景音乐',
            'icon': '🎵'
        },
        {
            'name': '设计模板',
            'slug': 'templates',
            'description': '设计模板文件',
            'icon': '📄'
        },
        {
            'name': '字体资源',
            'slug': 'fonts',
            'description': '中英文字体文件',
            'icon': '🔤'
        }
    ]

    # 创建子分类
    subcategories_data = {
        '图片素材': [
            {'name': '自然风景', 'slug': 'nature', 'icon': '🌲'},
            {'name': '城市建筑', 'slug': 'architecture', 'icon': '🏙️'},
            {'name': '人物肖像', 'slug': 'portrait', 'icon': '👤'},
            {'name': '商业科技', 'slug': 'business', 'icon': '💼'},
        ],
        '矢量图形': [
            {'name': '图标集', 'slug': 'icons', 'icon': '🔹'},
            {'name': '插画', 'slug': 'illustrations', 'icon': '🎨'},
            {'name': '图案背景', 'slug': 'patterns', 'icon': '🔲'},
        ]
    }

    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'slug': cat_data['slug'],
                'description': cat_data['description'],
                'icon': cat_data['icon']
            }
        )
        categories[cat_data['name']] = category
        if created:
            print(f"✅ 分类创建成功: {cat_data['name']}")

    # 创建子分类
    for parent_name, subcats in subcategories_data.items():
        parent = categories[parent_name]
        for subcat_data in subcats:
            subcategory, created = Category.objects.get_or_create(
                name=subcat_data['name'],
                parent=parent,
                defaults={
                    'slug': subcat_data['slug'],
                    'icon': subcat_data['icon']
                }
            )
            if created:
                print(f"✅ 子分类创建成功: {parent.name} -> {subcat_data['name']}")


def create_tags():
    """创建标签数据"""
    tags_data = [
        {'name': '免费', 'slug': 'free', 'color': '#27ae60'},
        {'name': '精选', 'slug': 'featured', 'color': '#e74c3c'},
        {'name': '新品', 'slug': 'new', 'color': '#3498db'},
        {'name': '热门', 'slug': 'popular', 'color': '#e67e22'},
        {'name': '商业用途', 'slug': 'commercial', 'color': '#9b59b6'},
        {'name': '个人用途', 'slug': 'personal', 'color': '#1abc9c'},
        {'name': '高清', 'slug': 'hd', 'color': '#34495e'},
        {'name': '4K', 'slug': '4k', 'color': '#d35400'},
        {'name': '简约', 'slug': 'minimal', 'color': '#7f8c8d'},
        {'name': '创意', 'slug': 'creative', 'color': '#f39c12'},
    ]

    for tag_data in tags_data:
        tag, created = Tag.objects.get_or_create(
            name=tag_data['name'],
            defaults={
                'slug': tag_data['slug'],
                'color': tag_data['color']
            }
        )
        if created:
            print(f"✅ 标签创建成功: {tag_data['name']}")


def create_sample_materials():
    """创建示例素材数据"""
    # 获取用户和分类
    admin_user = User.objects.get(username='admin')
    designer_user = User.objects.get(username='designer')
    photographer_user = User.objects.get(username='photographer')

    images_category = Category.objects.get(slug='images')
    nature_category = Category.objects.get(slug='nature')
    vectors_category = Category.objects.get(slug='vectors')
    videos_category = Category.objects.get(slug='videos')

    # 获取标签
    free_tag = Tag.objects.get(slug='free')
    featured_tag = Tag.objects.get(slug='featured')
    new_tag = Tag.objects.get(slug='new')
    hd_tag = Tag.objects.get(slug='hd')
    commercial_tag = Tag.objects.get(slug='commercial')

    materials_data = [
        {
            'title': '美丽的日落风景图片',
            'description': '高质量的日落风景摄影，适合用作背景或设计素材',
            'material_type': 'image',
            'author': photographer_user,
            'category': nature_category,
            'tags': [free_tag, featured_tag, hd_tag],
            'license_type': 'free',
            'price': 0.00,
            'dimensions': '1920x1080',
            'file_size': 2048576,
            'view_count': 156,
            'download_count': 89,
            'like_count': 45,
            'favorite_count': 23,
            'is_featured': True,
            'status': 'approved'
        },
        {
            'title': '简约商业图标集',
            'description': '包含50个简约风格的商业图标，矢量格式可编辑',
            'material_type': 'vector',
            'author': designer_user,
            'category': vectors_category,
            'tags': [commercial_tag, new_tag, featured_tag],
            'license_type': 'premium',
            'price': 29.99,
            'file_size': 512000,
            'view_count': 234,
            'download_count': 67,
            'like_count': 89,
            'favorite_count': 34,
            'is_featured': True,
            'status': 'approved'
        },
        {
            'title': '城市夜景延时摄影',
            'description': '4K分辨率的城市夜景延时摄影视频素材',
            'material_type': 'video',
            'author': photographer_user,
            'category': videos_category,
            'tags': [hd_tag, featured_tag],
            'license_type': 'premium',
            'price': 49.99,
            'dimensions': '3840x2160',
            'duration': 30.5,
            'file_size': 157286400,
            'view_count': 189,
            'download_count': 45,
            'like_count': 67,
            'favorite_count': 28,
            'is_featured': True,
            'status': 'approved'
        },
        {
            'title': '抽象几何背景图案',
            'description': '现代风格的抽象几何背景图案，适合网页设计',
            'material_type': 'image',
            'author': designer_user,
            'category': images_category,
            'tags': [free_tag, new_tag],
            'license_type': 'free',
            'price': 0.00,
            'dimensions': '2560x1440',
            'file_size': 1572864,
            'view_count': 98,
            'download_count': 56,
            'like_count': 34,
            'favorite_count': 12,
            'status': 'approved'
        },
        {
            'title': '手绘插画元素',
            'description': '可爱的手绘风格插画元素集合',
            'material_type': 'vector',
            'author': admin_user,
            'category': vectors_category,
            'tags': [free_tag, featured_tag],
            'license_type': 'free',
            'price': 0.00,
            'file_size': 768000,
            'view_count': 167,
            'download_count': 78,
            'like_count': 56,
            'favorite_count': 31,
            'status': 'approved'
        }
    ]

    for material_data in materials_data:
        tags = material_data.pop('tags')

        # 生成唯一slug
        base_slug = material_data['title'].replace(' ', '-').lower()
        slug = base_slug
        counter = 1
        while Material.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        material_data['slug'] = slug

        # 设置发布时间
        material_data['published_at'] = timezone.now() - timedelta(days=counter * 2)

        material = Material.objects.create(**material_data)
        material.tags.set(tags)

        print(f"✅ 素材创建成功: {material.title}")


def update_user_stats():
    """更新用户统计数据"""
    for user in User.objects.all():
        user.materials_count = user.materials.filter(status='approved').count()
        user.downloads_count = user.materials.aggregate(
            total_downloads=models.Sum('download_count')
        )['total_downloads'] or 0
        user.save()
    print("✅ 用户统计数据更新完成")


def main():
    """主函数"""
    print("🚀 开始初始化素材网站数据...")

    try:
        create_superuser()
        create_test_users()
        create_categories()
        create_tags()
        create_sample_materials()
        update_user_stats()

        print("\n🎉 数据初始化完成！")
        print("\n📋 可用账户:")
        print("   管理员: admin / admin123")
        print("   设计师: designer / designer123")
        print("   摄影师: photographer / photo123")
        print("   开发者: developer / dev123")
        print("\n🌐 访问地址:")
        print("   前端: http://localhost:3000")
        print("   后端API: http://localhost:8000/api/")
        print("   管理后台: http://localhost:8000/admin/")

    except Exception as e:
        print(f"❌ 初始化过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
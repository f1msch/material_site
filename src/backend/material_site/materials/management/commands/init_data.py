from django.core.management.base import BaseCommand
from materials.models import Category, Material, MaterialTag
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import os
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Initialize sample data for materials website'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化数据...')

        # 创建或获取测试用户
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': '测试',
                'last_name': '用户'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'创建测试用户: {user.username}')

        # 创建分类
        categories_data = [
            {'name': '背景图片', 'slug': 'background', 'description': '各种风格的背景图片素材'},
            {'name': '图标素材', 'slug': 'icons', 'description': '矢量图标和表情包素材'},
            {'name': 'UI界面', 'slug': 'ui', 'description': '用户界面设计模板和组件'},
            {'name': '电商设计', 'slug': 'ecommerce', 'description': '电商平台相关的设计素材'},
            {'name': '插画艺术', 'slug': 'illustration', 'description': '手绘和数字插画作品'},
            {'name': '社交媒体', 'slug': 'social-media', 'description': '社交媒体帖子模板'},
            {'name': '视频素材', 'slug': 'video', 'description': '视频剪辑和动画素材'},
            {'name': '音频素材', 'slug': 'audio', 'description': '音效和背景音乐'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'创建分类: {category.name}')

        # 创建素材数据
        materials_data = [
            {
                'title': '渐变背景图片集合',
                'description': '50+ 精美渐变背景图片，适用于网页设计和海报制作，包含多种色彩搭配',
                'category': categories['background'],
                'material_type': 'image',
                'price': 0,
                'is_free': True,
                'tags': ['渐变', '背景', '现代', '设计', '色彩'],
                'downloads': 1245,
                'likes': 567,
            },
            {
                'title': '企业UI设计套件',
                'description': '完整的企业级UI界面设计模板，包含100+组件，支持响应式设计',
                'category': categories['ui'],
                'material_type': 'psd',
                'price': 89.99,
                'is_free': False,
                'tags': ['UI', '企业', '组件', '设计系统', '响应式'],
                'downloads': 892,
                'likes': 423,
            },
            {
                'title': '扁平化图标包',
                'description': '200+ 扁平化设计风格图标，支持AI和SVG格式，适用于各种项目',
                'category': categories['icons'],
                'material_type': 'vector',
                'price': 0,
                'is_free': True,
                'tags': ['图标', '扁平化', '矢量', 'UI', '简约'],
                'downloads': 2156,
                'likes': 987,
            },
            {
                'title': '商业摄影图片',
                'description': '高清商业摄影图片，适用于广告和宣传材料，专业级质量',
                'category': categories['background'],
                'material_type': 'image',
                'price': 29.99,
                'is_free': False,
                'tags': ['摄影', '商业', '高清', '广告', '专业'],
                'downloads': 567,
                'likes': 234,
            },
            {
                'title': 'Banner设计模板',
                'description': '电商活动Banner设计模板，包含多种尺寸和节日主题',
                'category': categories['ecommerce'],
                'material_type': 'psd',
                'price': 49.99,
                'is_free': False,
                'tags': ['Banner', '电商', '营销', '模板', '节日'],
                'downloads': 1789,
                'likes': 645,
            },
            {
                'title': '手绘插画素材',
                'description': '原创手绘风格插画，适合儿童产品和文创设计，温暖治愈风格',
                'category': categories['illustration'],
                'material_type': 'vector',
                'price': 0,
                'is_free': True,
                'tags': ['手绘', '插画', '原创', '艺术', '治愈'],
                'downloads': 934,
                'likes': 512,
            },
            {
                'title': '社交媒体素材包',
                'description': 'Instagram、Facebook等社交媒体帖子模板，提升品牌形象',
                'category': categories['social-media'],
                'material_type': 'psd',
                'price': 39.99,
                'is_free': False,
                'tags': ['社交', '模板', '营销', '设计', '品牌'],
                'downloads': 1243,
                'likes': 678,
            },
            {
                'title': '自然风景视频素材',
                'description': '4K高清自然风景视频，适合背景和宣传片使用，多场景可选',
                'category': categories['video'],
                'material_type': 'video',
                'price': 79.99,
                'is_free': False,
                'tags': ['视频', '4K', '风景', '自然', '高清'],
                'downloads': 456,
                'likes': 189,
            },
            {
                'title': '科技感背景图',
                'description': '未来科技风格背景图片，包含光效和抽象元素',
                'category': categories['background'],
                'material_type': 'image',
                'price': 19.99,
                'is_free': False,
                'tags': ['科技', '未来', '光效', '抽象', '数字'],
                'downloads': 723,
                'likes': 321,
            },
            {
                'title': '移动端UI组件',
                'description': '专为移动端设计的UI组件库，支持iOS和Android风格',
                'category': categories['ui'],
                'material_type': 'psd',
                'price': 59.99,
                'is_free': False,
                'tags': ['移动端', 'UI', '组件', 'iOS', 'Android'],
                'downloads': 1102,
                'likes': 498,
            }
        ]

        # 创建素材
        for i, material_data in enumerate(materials_data):
            # 计算创建时间（模拟不同时间发布）
            created_at = datetime.now() - timedelta(days=random.randint(1, 30))

            material = Material.objects.create(
                title=material_data['title'],
                description=material_data['description'],
                category=material_data['category'],
                material_type=material_data['material_type'],
                price=material_data['price'],
                is_free=material_data['is_free'],
                file_size=random.randint(1024000, 52428800),  # 1MB - 50MB
                downloads=material_data['downloads'],
                likes=material_data['likes'],
                uploader=user,
                created_at=created_at
            )

            # 添加标签
            for tag_name in material_data['tags']:
                MaterialTag.objects.create(material=material, name=tag_name)

            self.stdout.write(f'创建素材: {material.title}')

        self.stdout.write(
            self.style.SUCCESS('✅ 数据初始化完成！')
        )
        self.stdout.write(f'创建了 {len(categories)} 个分类')
        self.stdout.write(f'创建了 {len(materials_data)} 个素材')
        self.stdout.write('测试用户: testuser / testpass123')
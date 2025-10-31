
确实，Django 的核心是模型和视图，但要想构建高效、可维护、安全的项目，还需要掌握一些高级技巧。以下是一些 Django 的高端技巧和最佳实践：

1. 数据库优化

使用 select_related 和 prefetch_related 减少数据库查询次数
```python
# 避免N+1查询问题
# 使用 select_related 用于外键和一对一关系
materials = Material.objects.select_related('category').all()

# 使用 prefetch_related 用于多对多和反向关系
materials = Material.objects.prefetch_related('tags').all()
```
使用 only 和 defer 控制字段的加载
```python
# 只加载需要的字段
materials = Material.objects.only('name', 'price')

# 排除不需要的字段（谨慎使用，因为可能会引起额外的查询）
materials = Material.objects.defer('description')
```
使用数据库索引
```python
class Material(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'category']),
        ]
```
2. 使用 Django 的缓存框架

视图缓存
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 缓存15分钟
def my_view(request):
    ...
```
模板片段缓存
```html
{% load cache %}
{% cache 500 sidebar %}
    .. sidebar ..
{% endcache %}
```
使用低级缓存API
```python
from django.core.cache import cache

def get_materials():
    materials = cache.get('all_materials')
    if not materials:
        materials = Material.objects.all()
        cache.set('all_materials', materials, 60*15)
    return materials
```
3. 异步任务

使用 Celery 处理异步任务
```python
# tasks.py
from celery import shared_task

@shared_task
def send_email():
    # 发送邮件
    pass
```
4. 安全性

使用 Django 的内置安全特性
* 使用 django.middleware.security.SecurityMiddleware 提供多种安全保护
* 使用 django.views.decorators.csrf.csrf_protect 防止 CSRF 攻击
* 使用 django.contrib.auth.mixins.LoginRequiredMixin 要求登录

密码哈希
```python
# 使用强密码哈希器
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
```
5. 自定义模型管理器和查询集

自定义查询集
```python
class MaterialQuerySet(models.QuerySet):
    def in_stock(self):
        return self.filter(stock__gt=0)

    def by_category(self, category):
        return self.filter(category=category)

class MaterialManager(models.Manager):
    def get_queryset(self):
        return MaterialQuerySet(self.model, using=self._db)

    def in_stock(self):
        return self.get_queryset().in_stock()

class Material(models.Model):
    # ... 字段定义
    objects = MaterialManager()
```
6. 信号（Signals）

使用信号在模型保存时执行操作
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Material)
def update_stock(sender, instance, created, **kwargs):
    if created:
        # 新物料创建时执行操作
        pass
```
7. 自定义中间件

创建自定义中间件
```python
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 处理请求
        response = self.get_response(request)
        # 处理响应
        return response
```
8. 使用 Django REST Framework 构建 API

视图集和路由
```python
from rest_framework import viewsets, routers

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

router = routers.DefaultRouter()
router.register('materials', MaterialViewSet)
```
自定义权限
```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```
9. 测试

编写测试用例
```python
from django.test import TestCase

class MaterialTestCase(TestCase):
    def setUp(self):
        Material.objects.create(name="Test Material", price=100)

    def test_material_creation(self):
        material = Material.objects.get(name="Test Material")
        self.assertEqual(material.price, 100)
```
使用工厂函数生成测试数据
```python
import factory
from .models import Material

class MaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Material

    name = factory.Sequence(lambda n: f"Material {n}")
    price = 100
```
10. 部署优化

使用 WhiteNoise 服务静态文件
```python
# settings.py
MIDDLEWARE = [
    # ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```
使用环境变量管理配置
```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', False)
```
11. 使用 Django Debug Toolbar 进行调试

安装和配置
```python
# settings.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```
12. 使用 Django Extensions

提供一些有用的管理命令
```bash
pip install django-extensions
python
# settings.py
INSTALLED_APPS = [
    ...,
    'django_extensions',
]
```
使用 runserver_plus 和 shell_plus
```bash
python manage.py runserver_plus
python manage.py shell_plus
```
13. 数据库连接池

使用 django-db-connections 或 django-db-geventpool 来管理数据库连接池
14. 使用 Django 的 F 表达式和 Q 对象

F 表达式用于在数据库层面进行操作
```python
from django.db.models import F

Material.objects.update(price=F('price') * 1.1)  # 将所有材料价格提高10%
```
Q 对象用于复杂查询
```python
from django.db.models import Q

Material.objects.filter(
    Q(category='metal') | Q(price__lt=100)
)
```
15. 自定义模板标签和过滤器
```python
# 在 templatetags 目录下创建自定义标签
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg
```
这些技巧可以帮助你构建更高效、可维护和安全的 Django 项目。当然，还有很多其他高级特性，根据项目需求选择使用。

当然有！Django 有很多"高端技巧"可以让你的代码更优雅、性能更好、维护性更强。让我分享一些真正提升水平的技巧：

## 🚀 性能优化技巧
1. 数据库查询优化
```python
# ❌ 糟糕的N+1查询
materials = Material.objects.all()
for material in materials:
    print(material.category.name)  # 每次循环都查询数据库

# ✅ 使用 select_related 和 prefetch_related
materials = Material.objects.select_related('category').prefetch_related('tags').all()
for material in materials:
    print(material.category.name)  # 一次查询搞定
```
2. 批量操作
```python
# ❌ 循环中逐个保存
for i in range(1000):
    Material.objects.create(name=f"Material {i}")

# ✅ 批量创建
materials = [Material(name=f"Material {i}") for i in range(1000)]
Material.objects.bulk_create(materials)  # 快10-100倍

# ✅ 批量更新
Material.objects.filter(price__lt=100).update(price=100)
```
3. 延迟加载和仅需字段
```python
# 只获取需要的字段
materials = Material.objects.only('id', 'name')  # 不加载description等大字段
materials = Material.objects.defer('description')  # 排除特定字段
```
## 🏗️ 架构设计技巧
4. 自定义Manager和QuerySet
```python
class MaterialQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def expensive(self):
        return self.filter(price__gte=1000)
    
    def by_category(self, category):
        return self.filter(category__name=category)

class MaterialManager(models.Manager):
    def get_queryset(self):
        return MaterialQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()

class Material(models.Model):
    # 字段定义...
    objects = MaterialManager()

# 使用
Material.objects.active().expensive().by_category('metal')
```
5. 服务层模式
```python
# services/material_service.py
class MaterialService:
    @staticmethod
    def create_material_with_tags(name, price, tags):
        with transaction.atomic():
            material = Material.objects.create(name=name, price=price)
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                material.tags.add(tag)
            return material
    
    @staticmethod
    def get_material_stats():
        return {
            'total': Material.objects.count(),
            'avg_price': Material.objects.aggregate(avg=Avg('price'))['avg'],
            'by_category': Material.objects.values('category').annotate(count=Count('id'))
        }

# 在views中使用
material = MaterialService.create_material_with_tags('Steel', 500, ['metal', 'construction'])
6. 数据迁移的优雅处理
python
# 在migrations中执行数据迁移
from django.db import migrations

def populate_initial_categories(apps, schema_editor):
    Category = apps.get_model('api', 'Category')
    Category.objects.bulk_create([
        Category(name='Metal', slug='metal'),
        Category(name='Plastic', slug='plastic'),
        Category(name='Wood', slug='wood'),
    ])

class Migration(migrations.Migration):
    dependencies = [...]
    
    operations = [
        migrations.RunPython(populate_initial_categories),
    ]
```
## 🔧 Django 高级特性
7. 信号(Signals)的合理使用
```python
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

@receiver(post_save, sender=Material)
def update_material_search_index(sender, instance, created, **kwargs):
    # 材料保存后更新搜索索引
    update_search_index(instance)

@receiver(pre_delete, sender=Material)
def cleanup_material_files(sender, instance, **kwargs):
    # 删除材料前清理相关文件
    if instance.image:
        instance.image.delete(save=False)
```
8. 条件查询的优雅写法
```python
from django.db.models import Q, Case, When, Value, IntegerField

# 复杂查询条件
materials = Material.objects.filter(
    Q(category__name='metal') | 
    Q(price__gte=100) |
    Q(name__icontains='premium')
).annotate(
    priority=Case(
        When(price__gte=1000, then=Value(1)),
        When(price__gte=500, then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )
).order_by('priority', 'name')
```
9. 自定义模板标签和过滤器
```python
# templatetags/material_extras.py
from django import template

register = template.Library()

@register.filter
def format_price(price):
    return f"¥{price:,.2f}"

@register.simple_tag
def material_stats():
    return Material.objects.aggregate(
        total=Count('id'),
        avg_price=Avg('price')
    )

# 模板中使用
{% load material_extras %}
{{ material.price|format_price }}
{% material_stats as stats %}
总计: {{ stats.total }}
```
## 🎯 生产环境技巧
10. 配置管理和环境分离
```python
# settings/__init__.py
import os
from .base import *

env = os.getenv('DJANGO_ENV', 'development')

if env == 'production':
    from .production import *
elif env == 'staging':
    from .staging import *
else:
    from .development import *

# settings/base.py - 通用配置
# settings/development.py - 开发环境
# settings/production.py - 生产环境
```
11. 自定义中间件
```python
# middleware/performance.py
import time
from django.utils.deprecation import MiddlewareMixin

class QueryCountMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        from django.db import connection
        if len(connection.queries) > 10:
            print(f"警告: 页面 {request.path} 执行了 {len(connection.queries)} 次查询")
        return response
```
12. 高级缓存策略
```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# 视图缓存
@cache_page(60 * 15)  # 15分钟
def material_list(request):
    # ...

# 模板片段缓存
{% load cache %}
{% cache 600 material_detail material.id %}
    {# 材料详情内容 #}
{% endcache %}

# 低级缓存API
def get_material_stats():
    stats = cache.get('material_stats')
    if not stats:
        stats = calculate_material_stats()  # 复杂计算
        cache.set('material_stats', stats, 60 * 60)  # 缓存1小时
    return stats
```
## 💡 测试和调试技巧
13. 工厂模式和测试数据
```python
# tests/factories.py
import factory
from .models import Material, Category

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")

class MaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Material
    
    name = factory.Sequence(lambda n: f"Material {n}")
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    category = factory.SubFactory(CategoryFactory)

# 在测试中使用
def test_material_creation():
    material = MaterialFactory(price=100)
    assert material.price == 100
```
14. Django Debug Toolbar 的高级使用
```python
# 配置更详细的调试信息
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'RESULTS_CACHE_SIZE': 100,
    'SQL_WARNING_THRESHOLD': 100,  # 超过100ms的查询显示警告
}
```
## 🎨 代码质量技巧
15. 类型提示和文档
```python
from typing import List, Dict, Optional
from django.db.models import QuerySet

class MaterialService:
    """材料服务类，处理材料相关的业务逻辑"""
    
    @staticmethod
    def get_materials_by_price_range(
        min_price: float, 
        max_price: float,
        category: Optional[str] = None
    ) -> QuerySet:
        """
        根据价格范围获取材料
        
        Args:
            min_price: 最低价格
            max_price: 最高价格  
            category: 可选分类名称
            
        Returns:
            材料查询集
        """
        queryset = Material.objects.filter(
            price__gte=min_price, 
            price__lte=max_price
        )
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset
```
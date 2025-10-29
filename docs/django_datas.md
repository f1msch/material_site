### 方法一：通过Django管理员后台添加
创建超级用户
python manage.py createsuperuser
用户名: admin
邮箱: admin@example.com
密码: ********
密码(重复): ********
Superuser created successfully.
登录管理员后台
python manage.py runserver
http://127.0.0.1:8000/admin/
### 方法二：使用Django Shell批量添加测试数据
python manage.py shell

```python
from django.contrib.auth.models import User
from blog.models import Category, Post
from django.utils import timezone

# 获取或创建用户
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()

# 创建分类
categories_data = [
    {'name': 'Python编程'},
    {'name': 'Web开发'},
    {'name': '数据库'},
    {'name': '前端技术'},
]

categories = {}
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(**cat_data)
    categories[cat_data['name']] = category
    print(f"创建分类: {category.name}")

# 创建博客文章
posts_data = [
    {
        'title': 'Django入门教程',
        'content': '''
        Django是一个高级Python Web框架，它鼓励快速开发和干净、实用的设计。
        
        ## 主要特点
        - 强大的ORM
        - 自动化的管理员界面
        - 优雅的URL设计
        - 模板系统
        - 缓存框架
        
        Django让Web开发变得愉快而高效。
        ''',
        'category': categories['Python编程'],
        'status': 'published'
    },
    {
        'title': 'Python列表推导式详解',
        'content': '''
        列表推导式是Python中非常强大的特性，可以简洁地创建列表。
        
        ### 基本语法
        ```python
        [expression for item in iterable if condition]
        ```
        
        ### 示例
        ```python
        # 生成1-10的平方
        squares = [x**2 for x in range(1, 11)]
        print(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        
        # 过滤偶数
        evens = [x for x in range(20) if x % 2 == 0]
        print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        ```
        ''',
        'category': categories['Python编程'],
        'status': 'published'
    },
    {
        'title': 'HTML5新特性介绍',
        'content': '''
        HTML5引入了许多新特性，使Web开发更加强大。
        
        ## 主要新特性
        - 语义化标签（header, footer, article, section等）
        - 音频视频支持
        - Canvas绘图
        - 本地存储
        - 地理定位
        
        HTML5让Web应用更加丰富和交互性更强。
        ''',
        'category': categories['前端技术'],
        'status': 'published'
    },
    {
        'title': 'PostgreSQL与Django集成',
        'content': '''
        PostgreSQL是一个功能强大的开源关系数据库。
        
        ## 在Django中的配置
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'mydatabase',
                'USER': 'mydatabaseuser',
                'PASSWORD': 'mypassword',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        ```
        
        PostgreSQL提供了JSON字段、全文搜索等高级功能。
        ''',
        'category': categories['数据库'],
        'status': 'published'
    }
]

for post_data in posts_data:
    post = Post.objects.create(
        title=post_data['title'],
        content=post_data['content'],
        author=user,
        category=post_data['category'],
        status=post_data['status'],
        published_at=timezone.now()
    )
    print(f"创建文章: {post.title}")

print("所有测试数据创建完成！")
```
exit()  # 退出Django Shell

### 方法三：创建自定义管理命令
```python
# blog/management/commands/add_sample_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post
from django.utils import timezone

class Command(BaseCommand):
    help = '添加示例博客数据'

    def handle(self, *args, **options):
        # 创建测试用户
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'is_staff': True
            }
        )
        if created:
            user.set_password('demopass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('创建用户: demo'))

        # 创建分类
        categories = [
            'Django教程',
            'Python技巧',
            '前端开发',
            '数据库'
        ]
        
        category_objects = {}
        for cat_name in categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            category_objects[cat_name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建分类: {cat_name}'))

        # 创建文章
        posts = [
            {
                'title': '欢迎来到Django博客',
                'content': '这是一个使用Django创建的博客系统示例。',
                'category': category_objects['Django教程']
            },
            {
                'title': 'Python虚拟环境使用指南',
                'content': '学习如何使用venv创建和管理Python虚拟环境。',
                'category': category_objects['Python技巧']
            },
            {
                'title': '响应式网页设计基础',
                'content': '了解如何使用CSS媒体查询创建响应式布局。',
                'category': category_objects['前端开发']
            }
        ]

        for post_data in posts:
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'content': post_data['content'],
                    'author': user,
                    'category': post_data['category'],
                    'status': 'published',
                    'published_at': timezone.now()
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建文章: {post_data["title"]}'))

        self.stdout.write(self.style.SUCCESS('示例数据添加完成！'))
```
python manage.py add_sample_data

### 通过编写一个数据迁移脚本或使用 fixtures
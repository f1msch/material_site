# create_test_data.py
from blog.models import Category, Post
from django.contrib.auth.models import User

# 创建用户
user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')

# 创建分类
cat1 = Category.objects.create(name='Python')
cat2 = Category.objects.create(name='Django')

# 创建文章
Post.objects.create(
    title='Django入门教程',
    content='这是Django入门教程的内容...',
    author=user,
    category=cat2,
    status='published'
)
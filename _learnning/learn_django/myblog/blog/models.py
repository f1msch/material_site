# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
import itertools

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # 添加这行
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    # 在 Django 中，prepopulated_fields 只在 Admin 后台有效，在 shell 或普通视图中不会自动生成。
    # 我们需要确保在模型层面处理 slug 的自动生成。
    def save(self, *args, **kwargs):
        """重写save方法，确保slug自动生成"""
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """生成唯一的slug"""
        # 基于标题生成基础slug
        base_slug = slugify(self.title)
        if not base_slug:  # 如果标题无法生成slug（比如全是中文标点）
            base_slug = 'post'

        # 如果基础slug不重复，直接使用
        if not Post.objects.filter(slug=base_slug).exists():
            return base_slug

        # 如果重复，添加数字后缀直到找到不重复的slug
        for i in itertools.count(1):
            candidate_slug = f"{base_slug}-{i}"
            if not Post.objects.filter(slug=candidate_slug).exists():
                return candidate_slug

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
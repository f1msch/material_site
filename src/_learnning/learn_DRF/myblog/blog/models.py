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

    #
    # # 在 Django 中，prepopulated_fields 只在 Admin 后台有效，在 shell 或普通视图中不会自动生成。
    # # 我们需要确保在模型层面处理 slug 的自动生成。
    def save(self, *args, **kwargs):
        """重写save方法，确保slug自动生成，避免递归"""
        # 检查是否需要生成slug
        if not self.slug:
            # 生成slug但不立即保存
            self.slug = self._generate_unique_slug()

        # 检查是否是新建对象
        if self._state.adding:
            # 新建对象，直接调用父类save
            super().save(*args, **kwargs)
        else:
            # 更新对象，确保不触发递归
            # 使用update_fields来明确指定更新的字段
            super().save(update_fields=['slug'] if not any(
                kwargs.get(key) for key in ['force_insert', 'force_update', 'update_fields']) else None, *args,
                         **kwargs)

    def _generate_unique_slug(self):
        """生成唯一的slug（内部方法）"""
        base_slug = slugify(self.title)
        if not base_slug:  # 如果标题无法生成slug
            base_slug = 'post'

        slug = base_slug
        counter = 1

        # 检查slug是否唯一
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

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

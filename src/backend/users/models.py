from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """扩展用户模型"""
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    website = models.URLField(blank=True, verbose_name='个人网站')
    credits = models.IntegerField(default=0, verbose_name='积分')

    # 统计字段
    materials_count = models.IntegerField(default=0, verbose_name='素材数量')
    downloads_count = models.IntegerField(default=0, verbose_name='被下载次数')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

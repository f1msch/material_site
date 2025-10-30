from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="描述")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Material(models.Model):
    MATERIAL_TYPES = [
        ('image', '图片'),
        ('vector', '矢量图'),
        ('psd', 'PSD模板'),
        ('video', '视频'),
        ('audio', '音频'),
    ]

    title = models.CharField(max_length=200, verbose_name="标题")
    description = models.TextField(verbose_name="描述")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES, verbose_name="素材类型")
    image_preview = models.ImageField(upload_to='material_previews/', verbose_name="预览图")
    file = models.FileField(upload_to='materials/', verbose_name="素材文件")
    file_size = models.BigIntegerField(default=0, verbose_name="文件大小")
    downloads = models.IntegerField(default=0, verbose_name="下载次数")
    likes = models.IntegerField(default=0, verbose_name="收藏数")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="价格")
    is_free = models.BooleanField(default=False, verbose_name="是否免费")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="上传者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "素材"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class MaterialTag(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
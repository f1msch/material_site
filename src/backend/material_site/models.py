from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """素材分类"""
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL标识')
    description = models.TextField(blank=True, verbose_name='分类描述')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='父级分类'
    )
    icon = models.CharField(max_length=100, blank=True, verbose_name='图标类名')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'categories'
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    @property
    def level(self):
        """获取分类层级"""
        if self.parent is None:
            return 0
        return self.parent.level + 1


class Tag(models.Model):
    """素材标签"""
    name = models.CharField(max_length=30, unique=True, verbose_name='标签名称')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='URL标识')
    color = models.CharField(max_length=7, default='#666666', verbose_name='标签颜色')

    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        db_table = 'tags'
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Material(models.Model):
    """素材主模型"""

    # 素材类型选择
    MATERIAL_TYPES = (
        ('image', '图片'),
        ('vector', '矢量图'),
        ('video', '视频'),
        ('audio', '音频'),
        ('template', '模板'),
        ('font', '字体'),
        ('other', '其他'),
    )

    # 审核状态选择
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('approved', '已发布'),
        ('rejected', '已拒绝'),
    )

    # 许可类型选择
    LICENSE_CHOICES = (
        ('free', '免费'),
        ('premium', '付费'),
        ('cc-by', 'CC BY'),
        ('cc-by-sa', 'CC BY-SA'),
    )

    # 基础信息
    title = models.CharField(max_length=200, verbose_name='素材标题')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='URL标识')
    description = models.TextField(blank=True, verbose_name='素材描述')
    material_type = models.CharField(
        max_length=20,
        choices=MATERIAL_TYPES,
        default='image',
        verbose_name='素材类型'
    )

    # 关联关系
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name='上传者'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='materials',
        verbose_name='分类'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='materials', verbose_name='标签')

    # 文件信息
    main_file = models.FileField(
        upload_to='materials/%Y/%m/%d/',
        verbose_name='主文件'
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='缩略图'
    )
    preview_image = models.ImageField(
        upload_to='previews/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='预览图'
    )

    # 元数据
    file_size = models.BigIntegerField(default=0, verbose_name='文件大小(字节)')
    dimensions = models.CharField(max_length=50, blank=True, verbose_name='尺寸/分辨率')
    duration = models.FloatField(null=True, blank=True, verbose_name='时长(秒)')  # 用于音视频

    # 权限和状态
    license_type = models.CharField(
        max_length=20,
        choices=LICENSE_CHOICES,
        default='free',
        verbose_name='许可类型'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        verbose_name='价格'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='状态'
    )
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')

    # 统计字段
    view_count = models.IntegerField(default=0, verbose_name='浏览数')
    download_count = models.IntegerField(default=0, verbose_name='下载数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    favorite_count = models.IntegerField(default=0, verbose_name='收藏数')

    # 时间戳
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')

    class Meta:
        db_table = 'materials'
        verbose_name = '素材'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'material_type']),
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['view_count', 'download_count']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 自动生成slug
        if not self.slug:
            self.slug = self._generate_unique_slug()

        # 自动设置文件大小
        if self.main_file and not self.file_size:
            self.file_size = self.main_file.size

        # 如果状态变为已发布，设置发布时间
        if self.status == 'approved' and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while Material.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    @property
    def file_size_display(self):
        """人类可读的文件大小"""
        if self.file_size == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = self.file_size
        while size >= 1024 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        return f"{size:.2f} {size_names[i]}"


class Favorite(models.Model):
    """用户收藏"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'favorites'
        unique_together = ['user', 'material']  # 防止重复收藏
        verbose_name = '收藏'
        verbose_name_plural = verbose_name


class DownloadHistory(models.Model):
    """下载记录"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='downloads')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='downloads')
    downloaded_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'download_history'
        verbose_name = '下载记录'
        verbose_name_plural = verbose_name

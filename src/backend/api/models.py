from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
import os


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")
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
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="上传者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # 新增图片专用字段
    image_width = models.IntegerField(default=0, verbose_name="图片宽度")
    image_height = models.IntegerField(default=0, verbose_name="图片高度")
    thumbnail = models.ImageField(upload_to='material_thumbnails/', null=True, blank=True, verbose_name="缩略图")

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

        # 如果是图片类型，处理图片信息并生成缩略图
        if self.material_type == 'image' and self.file:
            self.process_image_file()

    def process_image_file(self):
        """处理图片文件，获取尺寸并生成缩略图"""
        try:
            # 打开图片文件
            if self.file.name.lower().endswith(('.psd', '.eps', '.ai')):
                # 对于特殊格式，跳过处理或使用特殊方法
                return

            with Image.open(self.file) as img:
                # 获取图片尺寸
                self.image_width, self.image_height = img.size

                # 生成缩略图（仅在需要时）
                if not self.thumbnail:
                    self.generate_thumbnail(img)

                # 保存更新后的信息
                super().save(update_fields=['image_width', 'image_height', 'thumbnail'])

        except Exception as e:
            print(f"处理图片时出错: {e}")

    def generate_thumbnail(self, img=None):
        """生成缩略图"""
        thumbnail_size = (300, 300)

        try:
            if img is None:
                img = Image.open(self.file)

            # 创建缩略图
            img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)

            # 保存到内存
            thumb_io = BytesIO()

            # 根据格式保存
            if img.mode in ('RGBA', 'LA', 'P'):
                format = 'PNG'
                image_format = 'image/png'
                if img.mode == 'P':
                    img = img.convert('RGBA')
            else:
                format = 'JPEG'
                image_format = 'image/jpeg'
                img = img.convert('RGB')

            img.save(thumb_io, format, quality=85)

            # 生成文件名
            filename = os.path.basename(self.file.name)
            name, ext = os.path.splitext(filename)
            thumb_filename = f'{name}_thumbnail{".png" if format == "PNG" else ".jpg"}'

            # 保存缩略图
            self.thumbnail.save(
                thumb_filename,
                ContentFile(thumb_io.getvalue()),
                save=False
            )

        except Exception as e:
            print(f"生成缩略图时出错: {e}")

    def get_file_type_display(self):
        """获取文件类型显示名"""
        return dict(self.MATERIAL_TYPES).get(self.material_type, '未知')

    def get_image_urls(self):
        """获取图片相关的URL"""
        urls = {
            'preview': self.image_preview.url if self.image_preview else None,
            'file': self.file.url if self.file else None,
            'thumbnail': self.thumbnail.url if self.thumbnail else None,
        }
        return urls


class MaterialTag(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
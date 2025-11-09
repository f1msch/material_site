from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Material, Favorite

@receiver(post_save, sender=Material)
def update_user_materials_count(sender, instance, created, **kwargs):
    """更新用户的素材数量统计"""
    if created:
        instance.author.materials_count += 1
        instance.author.save()

@receiver(post_delete, sender=Material)
def decrease_user_materials_count(sender, instance, **kwargs):
    """减少用户的素材数量统计"""
    instance.author.materials_count -= 1
    instance.author.save()

@receiver(post_save, sender=Favorite)
def update_material_favorite_count(sender, instance, created, **kwargs):
    """更新素材的收藏计数"""
    if created:
        instance.material.favorite_count += 1
    else:
        instance.material.favorite_count -= 1
    instance.material.save()
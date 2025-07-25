# signals.py
from django.db.models.signals import post_save, post_delete, pre_save, m2m_changed
from django.dispatch import receiver
from django.core.cache import cache
from django.db import transaction
from .models import Product, Comment, Attribute, Category


def clear_related_cache(instance):
   
    if hasattr(instance, 'product'):
        cache_keys = [
            f'product_{instance.product.id}_details',
            f'category_{instance.product.subcategory.category.id}_products'
        ]
        for key in cache_keys:
            cache.delete(key)


@receiver([post_save, post_delete], sender=Product)
def handle_product_changes(sender, instance, **kwargs):

    cache_key = f'product_{instance.id}_details'
    cache.delete(cache_key)
    

    if instance.subcategory and instance.subcategory.category:
        cache_key = f'category_{instance.subcategory.category.id}_products'
        cache.delete(cache_key)


@receiver(pre_save, sender=Category)
def check_category_changes(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Category.objects.get(pk=instance.pk)
        if old_instance.title != instance.title:
            for product in Product.objects.filter(subcategory__category=instance):
                product.save(update_fields=['updated_at'])


@receiver(m2m_changed)
def handle_m2m_changes(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        if hasattr(instance, 'clear_cache'):
            instance.clear_cache()
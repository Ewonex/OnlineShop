from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    def ready(self):
        from .models import Review, Item
        @receiver(post_save, sender=Review)
        def update_item_rating(sender, instance, **kwargs):
            item = instance.item
            mark = Review.objects.filter(item=item).aggregate(mark=models.Avg('mark'))
            item.mark = mark['mark']
            item.save()




from .models import CustomUser , Account
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_account(sender, instance, created, **kwargs):
    if created and instance.user_type != 'BK':
        Account.objects.create(user=instance)
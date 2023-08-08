# signals.py
from django.db.models.signals import post_save
from user.models import User
from django.dispatch import receiver
import random
from .models import Myfolder

def list_number():
    return random.randint(100000, 999999)

@receiver(post_save, sender=User)
def create_user_myfolder(sender, instance, created, **kwargs):
    if created:
        Myfolder.objects.create(
            list_name='MY 달송', 
            user=instance,
            list_number=list_number()
        )

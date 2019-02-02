from django.db.models.signals import post_save
from users.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def save_profile(sender, instance, **kwards):
   instance.profile.save()
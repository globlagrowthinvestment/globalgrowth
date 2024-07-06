from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, MpesaMessage

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=MpesaMessage)
def update_user_balance(sender, instance, **kwargs):
    # Only update balance if the message is verified
    if instance.is_verified:
        user_profile = UserProfile.objects.get(user=instance.user)
        # Assuming the amount is part of MpesaMessage
        user_profile.balance += instance.amount
        user_profile.save()



from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_username = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    def get_total_referral_reward(self):
        from referrals.models import Referral  # Import here to avoid circular import
        return Referral.objects.filter(referrer=self.user).aggregate(Sum('reward_earned'))['reward_earned__sum'] or 0
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class ReferralProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = get_random_string(10)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s referral profile"

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referred_by')
    signup_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.referrer.username} referred {self.referred_user.username}"
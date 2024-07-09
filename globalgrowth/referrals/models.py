from django.db import models
from django.contrib.auth.models import User

class Referral(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    ]
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_made')
    referred = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_by')
    referral_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reward_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.referrer.username}'s referral - {self.referral_code}"

    @property
    def referred_username(self):
        return self.referred.username if self.referred else "N/A"

    @property
    def date_joined(self):
        return self.referred.date_joined if self.referred else None
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta



class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    total_investments = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_package_purchase = models.DateTimeField(null=True, blank=True)
    next_package_purchase_allowed = models.DateTimeField(null=True, blank=True)
    package = models.ForeignKey('whatsapp_rewards.Package', on_delete=models.SET_NULL, null=True, blank=True)
    package_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def can_buy_package(self):
        if not self.next_package_purchase_allowed:
            return True
        return timezone.now() >= self.next_package_purchase_allowed

    def is_package_active(self):
        if not self.package_expiry:
            return False
        return timezone.now() <= self.package_expiry



class UserTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)  # 'deposit', 'investment'
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Approval field
    verified = models.BooleanField(default=False)  # Verification field

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"



class MpesaMsg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'M-Pesa Message for {self.user.username}'

    class Meta:
        verbose_name = 'M-Pesa Message'
        verbose_name_plural = 'M-Pesa Messages'

from django.db import models
from django.contrib.auth.models import User


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    approved = models.BooleanField(default=False)  # Approval field
    verified = models.BooleanField(default=False)  # Verification field
    total_investments = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username

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

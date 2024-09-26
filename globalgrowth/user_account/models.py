from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_investments = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class UserTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)  # 'deposit' or 'investment'
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class MpesaMsg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def start_investment(self):
        self.start_date = timezone.now()
        self.end_date = self.start_date + timezone.timedelta(days=7)
        self.save()

    def is_matured(self):
        return timezone.now() >= self.end_date if self.end_date else False
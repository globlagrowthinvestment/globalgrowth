# models.py
from django.db import models
from django.contrib.auth.models import User

class PaymentAgent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)

class WithdrawalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal_requests')
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'), 
        ('approved', 'Approved'),
        ('declined', 'Declined'), 
        ('paid', 'Paid'),
        ('blocked', 'Blocked')
    ], default='pending')
    admin_comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
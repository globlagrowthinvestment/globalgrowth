# models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
        ('Error', 'Error')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.description} - {self.status}"

class MpesaMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add this field

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"

# Withdrawalsclass WithdrawalRequest(models.Model):
class WithdrawalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Add this line
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"

class MpesaTransaction(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
        ('Error', 'Error')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_id} - {self.status}"

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Open', choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.subject} - {self.status}"
    
    

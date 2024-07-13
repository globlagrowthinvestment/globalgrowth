from django.db import models
from django.contrib.auth.models import User

class Withdrawals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_number = models.CharField(max_length=255)
    requested_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Withdrawal request of {self.amount} KES by {self.user.username} on {self.requested_at}"




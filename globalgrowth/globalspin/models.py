from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Draw(models.Model):
    date = models.DateField(auto_now_add=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_draws')

    @property
    def is_active(self):
        now = timezone.now()
        return self.date == now.date() and self.start_time <= now.time() <= self.end_time

class TicketTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_message = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    draw = models.ForeignKey(Draw, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=10, unique=True)
    used = models.BooleanField(default=False)
    transaction = models.ForeignKey(TicketTransaction, on_delete=models.SET_NULL, null=True)
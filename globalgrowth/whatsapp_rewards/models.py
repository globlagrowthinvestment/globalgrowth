from django.db import models
from user_account.models import UserAccount
from django.utils import timezone
from datetime import timedelta


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # To control if the image should be displayed

    def __str__(self):
        return self.name or f"Product Image {self.id}"


class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    earnings_per_view = models.DecimalField(max_digits=10, decimal_places=2)
    max_views = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField(default=7)

    def __str__(self) -> str:
        return f'{self.name} {self.price} earn {self.earnings_per_view} bob per view'

class Status(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='statuses/')
    views = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def calculate_earnings(self):
        if self.views > self.package.max_views:
            return 0
        return self.views * self.package.earnings_per_view

    def is_expired(self):
        return timezone.now() > self.uploaded_at + timedelta(days=self.package.duration_days)

    def save(self, *args, **kwargs):
        self.earnings = self.calculate_earnings()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.package.name

class UserHistory(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(UserAccount, related_name='approved_by', null=True, blank=True, on_delete=models.SET_NULL)
    rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.status.package.name}"
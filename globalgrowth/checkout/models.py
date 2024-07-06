from django.db import models

class Package(models.Model):
    PACKAGE_CHOICES = [
        ('silver', 'Silver'),
        ('iron', 'Iron'),
        ('bronze', 'Bronze'),
        ('gold', 'Gold'),
        ('gold_pro', 'Gold Pro'),
        ('bronze_pro', 'Bronze Pro'),
        ('exceptional', 'Exceptional Package'),
        ('custom', 'Custom Package'),
    ]

    name = models.CharField(max_length=20, choices=PACKAGE_CHOICES)
    returns = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.get_name_display()
    
class MpesaPayment(models.Model):
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    result_code = models.IntegerField()
    result_desc = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=100)
    transaction_date = models.DateTimeField()
    phone_number = models.CharField(max_length=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"M-Pesa Payment {self.mpesa_receipt_number}"

    class Meta:
        ordering = ['-created_at']
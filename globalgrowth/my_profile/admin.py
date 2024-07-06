# admin.py

from django.contrib import admin
from .models import UserProfile, Transaction, MpesaMessage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'phone_number')
    search_fields = ('user__username', 'phone_number')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'amount', 'description', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'description')
    actions = ['mark_as_verified', 'mark_as_approved']

    def mark_as_verified(self, request, queryset):
        queryset.update(status='Verified')
        self.message_user(request, "Selected transactions have been marked as verified.")

    def mark_as_approved(self, request, queryset):
        for transaction in queryset:
            if transaction.status == 'Verified':
                transaction.status = 'Approved'
                transaction.save()
                user_profile = UserProfile.objects.get(user=transaction.user)
                user_profile.balance += transaction.amount
                user_profile.save()
        self.message_user(request, "Selected transactions have been marked as approved and balances updated.")

    mark_as_verified.short_description = "Mark selected transactions as verified"
    mark_as_approved.short_description = "Mark selected transactions as approved"

@admin.register(MpesaMessage)
class MpesaMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at', 'is_verified')
    list_filter = ('is_verified', 'submitted_at')
    search_fields = ('user__username', 'message')
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        for mpesa_message in queryset:
            mpesa_message.is_verified = True
            mpesa_message.save()

            # Update UserProfile balance
            user_profile = UserProfile.objects.get(user=mpesa_message.user)
            user_profile.balance += mpesa_message.amount
            user_profile.save()

        self.message_user(request, "Selected messages have been marked as verified and balances updated.")

    mark_as_verified.short_description = "Mark selected messages as verified"

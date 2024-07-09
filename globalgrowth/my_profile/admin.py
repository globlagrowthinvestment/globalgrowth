# admin.py

from django.contrib import admin
from .models import Complaint, UserProfile, Transaction, MpesaMessage


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

# complains section
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('subject', 'description', 'user__username')
    actions = ['mark_as_pending', 'mark_as_resolved', 'mark_as_closed']

    def mark_as_pending(self, request, queryset):
        queryset.update(status='Pending')
    mark_as_pending.short_description = "Mark selected complaints as Pending"

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='Resolved')
    mark_as_resolved.short_description = "Mark selected complaints as Resolved"

    def mark_as_closed(self, request, queryset):
        queryset.update(status='Closed')
    mark_as_closed.short_description = "Mark selected complaints as Closed"
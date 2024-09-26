from django.contrib import admin
from .models import UserAccount, UserTransaction, MpesaMsg, Investment

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'total_investments')
    search_fields = ('user__username',)

@admin.register(UserTransaction)
class UserTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'timestamp', 'approved')
    list_filter = ('transaction_type', 'approved')
    search_fields = ('user__username',)
    actions = ['approve_transactions']

    def approve_transactions(self, request, queryset):
        for transaction in queryset:
            if not transaction.approved:
                transaction.approved = True
                transaction.save()
                
                user_account = UserAccount.objects.get(user=transaction.user)
                if transaction.transaction_type == 'deposit':
                    user_account.balance += transaction.amount
                elif transaction.transaction_type == 'investment':
                    user_account.total_investments += transaction.amount
                    user_account.balance -= transaction.amount
                user_account.save()
        
        self.message_user(request, f"{queryset.count()} transactions were approved.")
    approve_transactions.short_description = "Approve selected transactions"

@admin.register(MpesaMsg)
class MpesaMsgAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')
    search_fields = ('user__username', 'message')

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'start_date', 'end_date', 'approved', 'completed')
    list_filter = ('approved', 'completed')
    search_fields = ('user__username',)
    actions = ['approve_investments', 'complete_investments']

    def approve_investments(self, request, queryset):
        for investment in queryset:
            if not investment.approved:
                investment.approved = True
                investment.save()
                
                user_account = UserAccount.objects.get(user=investment.user)
                user_account.balance -= investment.amount
                user_account.total_investments += investment.amount
                user_account.save()
        
        self.message_user(request, f"{queryset.count()} investments were approved.")
    approve_investments.short_description = "Approve selected investments"

    def complete_investments(self, request, queryset):
        for investment in queryset:
            if investment.approved and not investment.completed and investment.is_matured():
                investment.completed = True
                investment.save()
                
                user_account = UserAccount.objects.get(user=investment.user)
                user_account.balance += investment.amount * Decimal('1.1')  # 10% return
                user_account.total_investments -= investment.amount
                user_account.save()
        
        self.message_user(request, f"{queryset.count()} investments were completed.")
    complete_investments.short_description = "Complete matured investments"
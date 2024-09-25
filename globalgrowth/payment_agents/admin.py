from django.contrib import admin
from .models import WithdrawalRequest

@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'amount', 'status', 'created_at')
   
    search_fields = ('user__username', 'phone_number')
    
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            obj.admin_comment = f"Status changed to {obj.get_status_display()} by {request.user.username}"
        super().save_model(request, obj, form, change)
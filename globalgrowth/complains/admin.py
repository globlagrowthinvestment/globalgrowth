from django.contrib import admin
from .models import Complaint, AdminComment

class AdminCommentInline(admin.TabularInline):
    model = AdminComment
    extra = 1

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'complaint_type', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'complaint_type', 'created_at')
    search_fields = ('user__username', 'complaint_type', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AdminCommentInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'status' in form.changed_data:
            AdminComment.objects.create(
                complaint=obj,
                comment=f"Status changed to {obj.get_status_display()} by admin."
            )

@admin.register(AdminComment)
class AdminCommentAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('complaint__user__username', 'comment')
    readonly_fields = ('created_at',)
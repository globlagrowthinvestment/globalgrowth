from django.contrib import admin
from .models import Package, Status, UserHistory, ProductImage
from datetime import timezone

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)
    
class StatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'views', 'approved', 'earnings']
    actions = ['approve_status']

    def approve_status(self, request, queryset):
        for status in queryset:
            if status.views <= status.package.max_views:
                status.approved = True
                status.save()
                UserHistory.objects.create(
                    user=status.user,
                    status=status,
                    approved_at=timezone.now(),
                    approved_by=request.user
                )
            else:
                UserHistory.objects.create(
                    user=status.user,
                    status=status,
                    rejected=True,
                    rejection_reason="Views exceed package limit"
                )

        self.message_user(request, "Selected statuses have been approved/rejected.")

admin.site.register(Package)
admin.site.register(Status, StatusAdmin)
admin.site.register(UserHistory)
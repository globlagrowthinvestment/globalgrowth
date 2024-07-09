from .models import Referral
from django.contrib import admin
from .models import Referral

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_username', 'referral_code', 'status', 'reward_earned', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('referrer__username', 'referred__username', 'referral_code')
    actions = ['mark_as_active', 'mark_as_completed']
    
    def referred_username(self, obj):
        return obj.referred.username if obj.referred else "N/A"
    referred_username.short_description = "Referred User"

    def mark_as_active(self, request, queryset):
        queryset.update(status='ACTIVE')
    mark_as_active.short_description = "Mark selected referrals as active"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='COMPLETED')
    mark_as_completed.short_description = "Mark selected referrals as completed"

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('referrer', 'referred', 'referral_code')
        return ()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update the referrer's total reward
        total_reward = Referral.objects.filter(referrer=obj.referrer).aggregate(models.Sum('reward_earned'))['reward_earned__sum'] or 0
        obj.referrer.profile.total_referral_reward = total_reward
        obj.referrer.profile.save()
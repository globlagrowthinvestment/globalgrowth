from django.contrib import admin
from .models import ReferralProfile, Referral

@admin.register(ReferralProfile)
class ReferralProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'referral_code')
    search_fields = ('user__username', 'user__email', 'referral_code')

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_user', 'signup_date', 'is_active')
    list_filter = ('is_active', 'signup_date')
    search_fields = ('referrer__username', 'referrer__email', 'referred_user__username', 'referred_user__email')
    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Mark selected referrals as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected referrals as inactive"
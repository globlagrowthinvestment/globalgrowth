from django.contrib import admin
from django.db import models  # Add this import
from .models import Referral
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_username', 'referral_code', 'status', 'reward_earned', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('referrer__username', 'referred__username', 'referral_code')
    actions = ['mark_as_active', 'mark_as_completed', 'award_referral_bonus']

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

    def award_referral_bonus(self, request, queryset):
        for referral in queryset:
            # Add your logic to calculate and award bonus here, for example:
            bonus_amount = 10.00  # Example bonus amount
            referral.reward_earned += bonus_amount
            referral.save()

            # Update the referrer's total reward
            total_reward = Referral.objects.filter(referrer=referral.referrer).aggregate(models.Sum('reward_earned'))['reward_earned__sum'] or 0
            referral.referrer.profile.total_referral_reward = total_reward
            referral.referrer.profile.save()

            self.message_user(request, f"Bonus of {bonus_amount} awarded to {referral.referrer.username}'s referral {referral.referral_code}")

    award_referral_bonus.short_description = "Award referral bonus to selected referrals"

    def referral_detail_view(self, obj):
        return format_html('<a href="{}">View Referrals</a>', reverse('admin:view_referrals', args=[obj.referrer.id]))

    referral_detail_view.short_description = "Referrals Detail"
    list_display += ('referral_detail_view',)

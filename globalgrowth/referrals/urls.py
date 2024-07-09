from django.urls import path
from . import views

app_name = 'referrals'

urlpatterns = [
    path('referrals/', views.referral_dashboard, name='referrals'),
    # Add other URL patterns as needed
    path('referral/<str:referral_code>/', views.track_referral, name='track_referral'),
    path('complete-referral/', views.complete_referral, name='complete_referral'),
]
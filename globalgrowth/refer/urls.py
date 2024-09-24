from django.urls import path
from . import views

app_name = 'refer'

urlpatterns = [
    path('', views.referral_dashboard, name='referral_dashboard'),
]
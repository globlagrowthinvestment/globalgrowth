
from django.urls import path
from . import views

app_name = 'user_account'  # Set app_name to define the namespace

urlpatterns = [
    path('deposit/', views.deposit_view, name='deposit_money'),
    path('investments/', views.investment_view, name='package'),
    path('', views.profile_view, name='account_balance'),
    path('investment_growth/', views.investment_growth_view, name='investment_growth'),
    # Add other URL patterns as needed
]

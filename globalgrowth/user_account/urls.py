
from django.urls import path
from . import views

app_name = 'user_account'  # Set app_name to define the namespace

urlpatterns = [
    path('deposit/', views.deposit_view, name='deposit_money'),
    path('investments/', views.investment_view, name='package'),
    path('', views.profile_view, name='account_balance'),
    path('deposit/success/', views.deposit_success, name='deposit_success'),
    path('get_account_info/', views.get_account_info, name='get_account_info'),
    #path('investment_growth/', views.investment_growth_view, name='investment_growth'),
    path('start_investment/<int:investment_id>/', views.start_investment_timer, name='start_investment'),
    path('check_investment/<int:investment_id>/', views.check_investment_status, name='check_investment'),
    # Add other URL patterns as needed
]

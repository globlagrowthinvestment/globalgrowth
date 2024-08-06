from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('buy-ticket/', views.buy_ticket, name='buy_ticket'),
    path('spin-wheel/', views.spin_wheel, name='spin_wheel'),
    path('admin-approve-ticket/<int:transaction_id>/', views.admin_approve_ticket, name='admin_approve_ticket'),
]
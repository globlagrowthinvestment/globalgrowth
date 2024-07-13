# urls.py in your 'withdrawals' app

from django.urls import path
from . import views

app_name = 'withdrawals'  # Set app_name to define the namespace

urlpatterns = [
    path('withdrawal-request/', views.request_withdrawal, name='request_withdrawal'),
    # Add other URL patterns as needed
]


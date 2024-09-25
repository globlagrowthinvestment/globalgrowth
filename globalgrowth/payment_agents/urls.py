from django.urls import path
from . import views

app_name = 'payment_agents'

urlpatterns = [
    path('withdrawal-request/', views.withdrawal_request, name='withdrawal_request'),
]
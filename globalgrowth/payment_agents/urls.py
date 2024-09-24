# urls.py
from django.urls import path
from . import views

app_name = 'payment_agents'
urlpatterns = [
    path('', views.payment_agent_view, name='payment_agent_view'),
    path('list/', views.payment_agent_list, name='payment_agent_list'),
    path('detail/<int:pk>/', views.payment_agent_detail, name='payment_agent_detail'),
]
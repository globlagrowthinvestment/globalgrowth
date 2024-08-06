from django.urls import path
from .views import whatsapp_status

urlpatterns = [
    path('whatsapp_status/', whatsapp_status, name='whatsapp_status'),
   
]
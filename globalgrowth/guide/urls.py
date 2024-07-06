from django.urls import path
from . import views

app_name = 'landing'
urlpatterns = [
    path('guide/', views.guide, name='guide'),
]
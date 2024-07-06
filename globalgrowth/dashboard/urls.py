from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('invest/', views.invest, name='invest'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('complains/', views.complains, name='complains'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('guide/', views.guide, name='guide'),
    
]
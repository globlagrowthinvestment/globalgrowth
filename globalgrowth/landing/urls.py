from django.urls import path
from . import views

app_name = 'landing'
urlpatterns = [
    path('', views.home, name='index'),
    path('welcome/', views.welcome, name='welcome'),
   
]
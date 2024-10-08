from django.urls import include, path
from . import views  # This imports views from the current app (my_profile)
from auth_app.views import register_view  # Import only the register view from auth_app

app_name = 'my_profile'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('user/', views.user, name='user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('delete-transaction/', views.delete_transaction, name='delete_transaction'),
    path('refer/', views.refer, name='refer'),
    path('complains/', include('complains.urls')),
    path('instructions/', views.instructions, name='instructions'),
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
    #path('views_earn/', views.views_earn, name='whatsapp_status'),
    #path('request_withdrawal/', views.request_withdrawal, name='request_withdrawal'),
    #path('cancel_withdrawal/<int:transaction_id>/', views.cancel_withdrawal, name='cancel_withdrawal'),
]
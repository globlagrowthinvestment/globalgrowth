from django.urls import path
from . import views


app_name = 'checkout'

urlpatterns = [
    path('packages/', views.package_list, name='package_list'),
    path('initiate-payment/', views.initiate_stk_push, name='initiate_payment'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
    path('checkout/mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
    #path('process-payment/', views.process_payment, name='process_payment'),
    #path('payment-success/', views.payment_success, name='payment_success'),
    #path('payment-failure/', views.payment_failure, name='payment_failure'),
]
"""
URL configuration for globalgrowth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('auth_app/', include('auth_app.urls')),
    path('refer/', include('refer.urls')),
    path('checkout/', include('checkout.urls')),
    path('complains/', include('complains.urls')),
    path('profile/', include('my_profile.urls')),
    path('withdraw/', include('withdrawals.urls')),
    path('account/', include('user_account.urls')),
    path('payment-agents/', include('payment_agents.urls', namespace='payment_agents')),
    path('views_earn/', include('whatsapp_rewards.urls')),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

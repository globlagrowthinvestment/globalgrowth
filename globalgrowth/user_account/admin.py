from django.contrib import admin
from .models import UserTransaction,UserAccount, MpesaMsg

admin.site.register(UserTransaction)
admin.site.register(UserAccount)
admin.site.register(MpesaMsg)

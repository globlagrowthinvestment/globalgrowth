from django.contrib import admin
from .models import Ticket, TicketTransaction, Draw

admin.site.register(Ticket)
admin.site.register(TicketTransaction)
admin.site.register(Draw)
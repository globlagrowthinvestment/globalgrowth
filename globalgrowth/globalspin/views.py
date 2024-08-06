from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Draw, Ticket, TicketTransaction
from django.http import JsonResponse
import random

@login_required
def dashboard(request):
    user_tickets = Ticket.objects.filter(user=request.user, used=False)
    active_draw = Draw.objects.filter(date=timezone.now().date(), end_time__gt=timezone.now().time()).first()
    return render(request, 'globalspin/dashboard.html', {'tickets': user_tickets, 'active_draw': active_draw})

@login_required
def buy_ticket(request):
    if request.method == 'POST':
        mpesa_message = request.POST.get('mpesa_message')
        transaction = TicketTransaction.objects.create(
            user=request.user,
            amount=500,  # Assuming fixed price
            mpesa_message=mpesa_message
        )
        return redirect('dashboard')
    return render(request, 'globalspin/buy_ticket.html')

@login_required
def spin_wheel(request):
    active_draw = Draw.objects.filter(date=timezone.now().date(), end_time__gt=timezone.now().time()).first()
    if not active_draw:
        return JsonResponse({'error': 'No active draw'})

    user_ticket = Ticket.objects.filter(user=request.user, draw=active_draw, used=False).first()
    if not user_ticket:
        return JsonResponse({'error': 'No valid ticket'})

    user_ticket.used = True
    user_ticket.save()

    # Simulate wheel spin
    prizes = [300, 2000, 7000, 200, 800, 100, 3000, 200, 400, 10000, 700, 500, 1000, 300, 400, 5000]
    winning_prize = random.choice(prizes)

    if winning_prize == 10000:  # Assuming 10000 is the jackpot
        active_draw.winner = request.user
        active_draw.save()

    return JsonResponse({'prize': winning_prize})

@login_required
def admin_approve_ticket(request, transaction_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    transaction = TicketTransaction.objects.get(id=transaction_id)
    transaction.approved = True
    transaction.save()

    # Create a new ticket for the user
    active_draw = Draw.objects.filter(date=timezone.now().date(), end_time__gt=timezone.now().time()).first()
    if active_draw:
        Ticket.objects.create(
            user=transaction.user,
            draw=active_draw,
            ticket_number=f"T{random.randint(1000, 9999)}",
            transaction=transaction
        )

    return JsonResponse({'success': True})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import UserAccount, UserTransaction, MpesaMsg, Investment
from decimal import Decimal
import re
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserAccount

@login_required
def profile_view(request):
    try:
        user_profile = UserAccount.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # Create a new UserAccount if it does not exist
        user_profile = UserAccount.objects.create(user=request.user)
    
    transactions = UserTransaction.objects.filter(user=request.user).order_by('-timestamp')
    investments = Investment.objects.filter(user=request.user, approved=True, completed=False)

    context = {
        'user_profile': user_profile,
        'transactions': transactions,
        'investments': investments,
    }
    return render(request, 'user_account/profile.html', context)

@login_required
def deposit_view(request):
    if request.method == 'POST':
        mpesa_message = request.POST.get('mpesa_message', '')
        MpesaMsg.objects.create(user=request.user, message=mpesa_message)
        
        amount_match = re.search(r'Ksh([\d,]+\.\d{2})', mpesa_message)
        if amount_match:
            amount = Decimal(amount_match.group(1).replace(',', ''))
            transaction = UserTransaction(user=request.user, amount=amount, transaction_type='deposit')
            transaction.save()
            
            # Redirect to success page with a message
            return redirect('user_account:deposit_success')  # Redirect to the success page after deposit
            
        else:
            return render(request, 'user_account/deposit_failed.html', {'message': 'Invalid M-Pesa message format.'})
    
    return render(request, 'user_account/deposit_form.html')

@login_required
def deposit_success(request):
    return render(request, 'user_account/success.html')


@login_required
def investment_view(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', 0))
        try:
            user_account = UserAccount.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User account not found.'})
        
        if amount <= 0 or amount > user_account.balance:
            return JsonResponse({'status': 'error', 'message': 'Invalid investment amount.'})
        
        investment = Investment(user=request.user, amount=amount)
        investment.save()
        
        return JsonResponse({'status': 'success', 'message': 'Investment submitted successfully. Pending approval.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def start_investment_timer(request, investment_id):
    try:
        investment = Investment.objects.get(id=investment_id, user=request.user, approved=True, completed=False)
        investment.start_investment()
        return JsonResponse({'status': 'success', 'message': 'Investment timer started.'})
    except Investment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Investment not found or not ready to start.'})

@login_required
def check_investment_status(request, investment_id):
    try:
        investment = Investment.objects.get(id=investment_id, user=request.user, approved=True, completed=False)
        if investment.is_matured():
            investment.completed = True
            investment.save()
            
            user_account = UserAccount.objects.get(user=request.user)
            user_account.balance += investment.amount * Decimal('1.1')  # 10% return
            user_account.total_investments -= investment.amount
            user_account.save()
            
            return JsonResponse({'status': 'success', 'message': 'Investment completed. Funds added to your balance.'})
        else:
            time_left = investment.end_date - timezone.now()
            return JsonResponse({'status': 'ongoing', 'time_left': str(time_left)})
    except Investment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Investment not found.'})

@login_required
def get_account_info(request):
    user_account = UserAccount.objects.get(user=request.user)
    return JsonResponse({
        'balance': str(user_account.balance),
        'total_deposits': str(user_account.total_deposits),
        'total_investments': str(user_account.total_investments)
    })
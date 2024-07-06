# views.py

import re
import hashlib
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from .forms import WithdrawalRequestForm
from .models import UserProfile, Transaction, MpesaMessage, MpesaTransaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Complaint
#from .forms import WithdrawalRequestForm
from .models import WithdrawalRequest
from django.utils import timezone





@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        mpesa_message = request.POST.get('mpesa_message')
        amount = extract_amount_from_mpesa(mpesa_message)
        if amount:
            # Convert amount to Decimal
            amount = Decimal(amount)
            
            # Check if the message already exists to prevent duplicates
            if MpesaMessage.objects.filter(user=request.user, message=mpesa_message).exists():
                messages.error(request, 'This M-Pesa message has already been submitted.')
            else:
                # Create MpesaMessage
                MpesaMessage.objects.create(user=request.user, message=mpesa_message)
                
                # Create transaction (pending verification)
                Transaction.objects.create(user=request.user, amount=amount, description="M-Pesa Deposit", status="Pending")
                
                messages.success(request, f'Your M-Pesa message has been submitted. Ksh {amount} will be credited to your account after admin verification.')
        else:
            messages.error(request, 'Invalid M-Pesa message. Please try again.')
    
    # Calculate the balance including only approved transactions
    total_deposits = Transaction.objects.filter(user=request.user, amount__gt=0, status='Approved').aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
    total_withdrawals = abs(Transaction.objects.filter(user=request.user, amount__lt=0, status='Approved').aggregate(Sum('amount'))['amount__sum'] or Decimal(0))
    balance = total_deposits - total_withdrawals

    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]
    
    for transaction in recent_transactions:
        if transaction.status == 'Approved':
            transaction.status_color = 'green'
        elif transaction.status == 'Verified':
            transaction.status_color = 'blue'
        else:
            transaction.status_color = 'yellow'
    
    # Generate Gravatar URL
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(request.user.email.lower().encode('utf8')).hexdigest() + "?s=80&d=mp"
    
    context = {
        'user_profile': user_profile,
        'balance': balance,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'recent_transactions': recent_transactions,
        'gravatar_url': gravatar_url,
    }
    return render(request, 'my_profile/profile.html', context)

@login_required
def request_withdrawal(request):
    if request.method == 'POST':
        form = WithdrawalRequestForm(request.POST)
        if form.is_valid():
            withdrawal_request = form.save(commit=False)
            withdrawal_request.user = request.user
            withdrawal_request.status = 'pending'

            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.balance >= withdrawal_request.amount:
                withdrawal_request.save()
                messages.success(request, 'Withdrawal request submitted successfully. Awaiting admin approval.')
                return redirect('my_profile/profile')  # Make sure 'profile' is the correct name for your profile URL
            else:
                messages.error(request, 'Insufficient balance for this withdrawal.')
        else:
            messages.error(request, 'Invalid form submission. Please check the form and try again.')
    else:
        form = WithdrawalRequestForm()

    return render(request, 'my_profile/request_withdrawal.html', {'form': form})
'''

'''
def extract_amount_from_mpesa(message):
    match = re.search(r'Ksh([\d,]+\.\d{2})', message)
    if match:
        return float(match.group(1).replace(',', ''))
    return None

@login_required
def payment_agents(request):
    return render(request, 'my_profile/payment_agents.html')

@login_required
def user(request):
    # Your view logic here
    return render(request, 'my_profile/user.html')

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully.')
    return redirect('profile')

@login_required
def complaints(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        Complaint.objects.create(user=request.user, subject=subject, description=description)
        return redirect('my_profile/complaints.html')

    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_profile/complaints.html', {'complaints': complaints})


def submit_complaint(request):
    # Your submit complaint view logic here
    pass

def guide(request):
    return render(request, 'my_profile/guide.html')

def dashboard1(request):
    return render(request, 'my_profile/dashboard1.html')

def instructions(request):
    return render(request, 'my_profile/instructions.html')

def invest(request):
    return render(request, 'my_profile/invest.html')

def referral(request):
    return render(request, 'my_profile/referral.html')


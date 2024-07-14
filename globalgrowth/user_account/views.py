from django.shortcuts import render, redirect
from .models import UserAccount, UserTransaction, MpesaMsg
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.db.models import Sum 
from datetime import datetime, timedelta
import json
import re

@login_required
def profile_view(request):
    try:
        user_profile = UserAccount.objects.get(user=request.user)
        transactions = UserTransaction.objects.filter(user=request.user).order_by('-timestamp')

        # Calculate total deposits and total investments
        total_deposits = UserTransaction.objects.filter(user=request.user, transaction_type='deposit').aggregate(total=Sum('amount'))['total']
        total_investments = UserTransaction.objects.filter(user=request.user, transaction_type='investment').aggregate(total=Sum('amount'))['total']

        # Convert None to Decimal('0.00')
        total_deposits = total_deposits if total_deposits is not None else Decimal('0.00')
        total_investments = total_investments if total_investments is not None else Decimal('0.00')

        context = {
            'user_profile': user_profile,
            'transactions': transactions,
            'total_deposits': total_deposits,
            'total_investments': total_investments,
        }
        return render(request, 'user_account/profile.html', context)
    except ObjectDoesNotExist:
        return render(request, 'user_account/profile.html', {'error_message': 'User account not found.'})
    except Exception as e:
        return render(request, 'user_account/profile.html', {'error_message': str(e)})


@login_required
def deposit_view(request):
    if request.method == 'POST':
        mpesa_message = request.POST.get('mpesa_message', '')
        
        # Save M-Pesa message to database
        MpesaMsg.objects.create(user=request.user, message=mpesa_message)
        
        # Extract amount from M-Pesa message using regex
        amount_match = re.search(r'Ksh([\d,]+\.\d{2})', mpesa_message)
        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')  # Remove commas if present
            amount = Decimal(amount_str)
            
            try:
                user_profile = UserAccount.objects.get(user=request.user)
            except UserAccount.DoesNotExist:
                user_profile = UserAccount.objects.create(user=request.user, balance=Decimal('0.00'))
            
            user_profile.balance += amount
            user_profile.save()
            
            transaction = UserTransaction(user=request.user, amount=amount, transaction_type='deposit')
            transaction.save()
            
            return redirect('user_account:account_balance')
        else:
            # Handle invalid M-Pesa message format
            return render(request, 'user_account/profile.html', {'error_message': 'Invalid M-Pesa message format. Please paste the correct message.'})
    

    return redirect('user_account:account_balance')



@login_required
def investment_view(request):
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        
        # Validate amount_str
        if not amount_str:
            return redirect('user_account:account_balance')

        try:
            amount = Decimal(amount_str)  # Convert amount to Decimal
            
            user_profile = UserAccount.objects.get(user=request.user)
            
            # Check if the account balance is sufficient
            if user_profile.balance < amount:
                return redirect('user_account:account_balance')
            
            # Check if account balance is zero
            if user_profile.balance == Decimal('0'):
                return redirect('user_account:account_balance')
            
            # Perform the investment
            user_profile.balance -= amount
            user_profile.total_investments += amount  # Update total investments
            user_profile.save()
            
            transaction = UserTransaction(user=request.user, amount=amount, transaction_type='investment')
            transaction.save()
            
            return redirect('user_account:account_balance')
        
        except Decimal.InvalidOperation:
            return redirect('user_account:account_balance')
        except UserAccount.DoesNotExist:
            # Handle the case where UserAccount does not exist for this user
            # For example, you could create a new UserAccount here
            user_profile = UserAccount.objects.create(user=request.user, balance=Decimal('0'))
            return redirect('user_account:account_balance')
        except Exception:
            return redirect('user_account:account_balance')
    return redirect('user_account:account_balance')




def investment_growth_view(request):
    # Calculate date 7 days ago from today
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    # Query investment transactions within the last 7 days
    investment_transactions = UserTransaction.objects.filter(
        user=request.user,
        transaction_type='investment',
        timestamp__gte=seven_days_ago
    ).order_by('timestamp')
    
    # Prepare data for the graph (using timestamps and amounts)
    labels = []
    data = []
    
    for transaction in investment_transactions:
        labels.append(transaction.timestamp.strftime('%Y-%m-%d %H:%M'))
        data.append(float(transaction.amount))  # Convert Decimal to float for JSON serialization
    
    context = {
        'labels': json.dumps(labels),  # Convert list to JSON format for JavaScript
        'data': json.dumps(data),      # Convert list to JSON format for JavaScript
    }
    
    return render(request, 'user_account/investment_growth.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WithdrawalRequest
from .forms import WithdrawalRequestForm

@login_required
def withdrawal_request(request):
    if request.method == 'POST':
        form = WithdrawalRequestForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            withdrawal.save()
            messages.success(request, 'Withdrawal request submitted successfully.')
            return redirect('payment_agents:withdrawal_request')
    else:
        form = WithdrawalRequestForm()
    
    requests = WithdrawalRequest.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'form': form,
        'requests': requests,
    }
    return render(request, 'payment_agents/withdrawal_request.html', context)
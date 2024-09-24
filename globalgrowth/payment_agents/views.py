from django.shortcuts import render, redirect
from .models import WithdrawalRequest, PaymentAgent
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def payment_agent_view(request):
    payment_agents = PaymentAgent.objects.all()
    requests = WithdrawalRequest.objects.filter(user=request.user)

    if request.method == 'POST':
        payment_agent = PaymentAgent.objects.get(id=request.POST['payment_agent'])
        phone_number = request.POST['phone_number']
        amount = request.POST['amount']
        request_obj = WithdrawalRequest.objects.create(
            user=request.user, 
            payment_agent=payment_agent,
            phone_number=phone_number,
            amount=amount
        )
        return redirect('payment_agent_view')

    return render(request, 'payment_agents/payment_agent.html', {
        'payment_agents': payment_agents,
        'requests': requests
    })

@user_passes_test(lambda u: u.is_staff)
def payment_agent_list(request):
    requests = WithdrawalRequest.objects.all()
    return render(request, 'payment_agent_list.html', {'requests': requests})

@user_passes_test(lambda u: u.is_staff)
def payment_agent_detail(request, pk):
    request_obj = WithdrawalRequest.objects.get(pk=pk)
    if request.method == 'POST':
        request_obj.status = request.POST['status']
        request_obj.admin_comment = request.POST['admin_comment']
        request_obj.save()
        return redirect('payment_agent_list')
    return render(request, 'payment_agent_detail.html', {'request': request_obj})

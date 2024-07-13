from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Withdrawals
from django.core.mail import send_mail

@login_required
def request_withdrawal(request):
    if request.method == 'GET':
        withdrawal_requests = Withdrawals.objects.filter(user=request.user).order_by('-id')
        return render(request, 'withdrawals/withdrawals.html', {'withdrawal_requests': withdrawal_requests}) 
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        mpesa_number = request.POST.get('mpesa_number')
        
        # Validate amount and mpesa_number if needed
        # Perform additional business logic if required
        
        # Create a new withdrawal request
        withdrawal_request = Withdrawals.objects.create(
            user=request.user,  
            amount=amount,
            mpesa_number=mpesa_number  # Save the MPESA number to your model
            # Add more fields as needed
        )


        
        # Send email notification
        """ send_email_notification(request.user.email, amount, mpesa_number) """
        
        messages.success(request, 'Withdrawal request submitted successfully.')
        return redirect('withdrawals:request_withdrawal') 
    else:
        # Handle GET request or invalid requests here if needed
        return redirect('my_profile:profile')  # Redirect to profile page or another appropriate URL

def send_email_notification(recipient_email, amount, mpesa_number):
    subject = 'Withdrawal Request Submitted'
    message = f'Withdrawal request for {amount} KES to MPESA number {mpesa_number} has been requested successfully by'
    from_email = 'your_email@gmail.com'  # Replace with your Gmail address
    recipient_list = [recipient_email]
    
    send_mail(subject, message, from_email, recipient_list)





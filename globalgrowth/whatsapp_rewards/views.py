from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Status, Package, UserHistory, ProductImage
from .forms import StatusForm
from .models import Status, UserAccount

@login_required
def whatsapp_status(request):
    try:
        # Fetch or create the UserAccount instance for the current user
        user_account, created = UserAccount.objects.get_or_create(user=request.user)
        account_balance = user_account.balance
    except UserAccount.DoesNotExist:
        # Handle this case if needed
        messages.info(request, "Your account was not found, so a new one was created.")
        user_account = UserAccount.objects.create(user=request.user)
        account_balance = user_account.balance

    if request.method == 'POST':
        form = StatusForm(request.POST, request.FILES)
        if form.is_valid():
            status = form.save(commit=False)
            package = status.package
            package_cost = package.price

            # Check if the user has sufficient balance
            if account_balance >= package_cost:
                # Deduct the cost from the user's account balance
                user_account.balance -= package_cost
                user_account.save()

                # Assign the UserAccount instance to the status
                status.user = user_account
                status.save()
                
                messages.success(request, 'Status uploaded successfully and balance updated.')
                return redirect('whatsapp_status')  # Redirect to the same view to display updated data
            else:
                messages.error(request, 'Insufficient balance to upload status.')
    else:
        form = StatusForm()

    # Filter Status objects and calculate total earnings
    statuses = Status.objects.filter(user=user_account)
    total_earnings = sum(status.earnings for status in statuses)

    #fetch the product add image
    images = ProductImage.objects.filter(is_active=True)
    print(images)

    # Fetch user history for the current user
    user_history = UserHistory.objects.filter(user=user_account)

    return render(request, 'whatsapp_rewards/whatsapp_status.html', {
        'form': form,
        'statuses': statuses,
        'total_earnings': total_earnings,
        'balance': account_balance,
        'user_history': user_history,
        'images' : images,
    })





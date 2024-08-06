from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Status, Package, UserHistory, ProductImage, UserAccount
from .forms import StatusForm

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
       
            if user_account.is_package_active():
                # Allow the user to upload an image without deducting balance
                messages.success(request, 'You have an active package. You can upload images without additional charges before package expiry.')
                # Continue processing the image upload here
                # Assign the UserAccount instance to the status
                status.user = user_account
                status.save()
                messages.success(request, 'Status uploaded successfully.')
                return redirect('whatsapp_status')  # Redirect to the same view to display updated data
            else:
                # Check if the user can buy a new package
                if not user_account.can_buy_package():
                    messages.error(request, 'You need to wait before buying a new package.')
                    return redirect('whatsapp_status')

                # User can buy a new package, proceed with purchase
                if account_balance >= package.price:
                    # Deduct the cost from the user's account balance
                    user_account.balance -= package.price
                    user_account.package_expiry = timezone.now() + timedelta(days=package.duration_days)
                    user_account.next_package_purchase_allowed = timezone.now() + timedelta(days=7)  # Next purchase allowed after 7 days
                    user_account.last_package_purchase = timezone.now()
                    user_account.save()

                    # Assign the UserAccount instance to the status
                    status.user = user_account
                    status.save()

                    messages.success(request, 'Status uploaded successfully and balance updated.')
                else:
                    messages.error(request, 'Insufficient balance to upload status.')

                return redirect('whatsapp_status')  # Redirect to the same view to display updated data
    else:
        form = StatusForm()

    # Filter Status objects and calculate total earnings
    statuses = Status.objects.filter(user=user_account)
    total_earnings = sum(status.earnings for status in statuses)

    # Fetch product images
    images = ProductImage.objects.filter(is_active=True)

    # Fetch user history for the current user
    user_history = UserHistory.objects.filter(user=user_account)

    # Prepare data for template
    context = {
        'form': form,
        'statuses': statuses,
        'total_earnings': total_earnings,
        'balance': account_balance,
        'user_history': user_history,
        'images': images,
        'can_upload_image': user_account.is_package_active(),
        'remaining_days': max(0, (user_account.package_expiry - timezone.now()).days) if user_account.package_expiry else 0,
        'show_add' : user_account.is_package_active(),
    }

    return render(request, 'whatsapp_rewards/whatsapp_status.html', context)

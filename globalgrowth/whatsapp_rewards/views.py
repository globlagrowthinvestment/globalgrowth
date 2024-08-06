from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Status, Package, UserHistory, ProductImage, UserAccount
from .forms import StatusForm, PackagePurchaseForm

@login_required
def whatsapp_status(request):
    user_account, created = UserAccount.objects.get_or_create(user=request.user)
    account_balance = user_account.balance
    active_package = user_account.package

    # Initialize forms
    package_form = PackagePurchaseForm()
    status_form = StatusForm()

    if request.method == 'POST':
        if 'buy_package' in request.POST:
            # Handle package purchase
            package_form = PackagePurchaseForm(request.POST)
            if package_form.is_valid():
                package = package_form.cleaned_data['package']
                
                if user_account.can_buy_package() and account_balance >= package.price:
                    user_account.balance -= package.price
                    user_account.package = package
                    user_account.package_expiry = timezone.now() + timedelta(days=package.duration_days)
                    user_account.next_package_purchase_allowed = timezone.now() + timedelta(days=7)
                    user_account.last_package_purchase = timezone.now()
                    user_account.save()
                    
                    messages.success(request, 'Package purchased successfully. Your balance has been updated.')
                    return redirect('whatsapp_status')  # Redirect to the same page to avoid form resubmission

                else:
                    messages.error(request, 'You cannot buy the package. Check your balance or wait for the allowed purchase time.')

        elif 'upload_status' in request.POST:
            # Handle status upload
            if user_account.is_package_active():
                status_form = StatusForm(request.POST, request.FILES)
                if status_form.is_valid():
                    status = status_form.save(commit=False)
                    status.package = user_account.package
                    status.user = user_account
                    status.save()
                    messages.success(request, 'Status uploaded successfully.')
                    return redirect('whatsapp_status')  # Redirect to the same page to avoid form resubmission
                else:
                    messages.error(request, 'Please correct the errors below.')
            else:
                messages.error(request, 'You do not have an active package. Please buy a package to upload statuses.')
                
    # Fetch data for the context
    statuses = Status.objects.filter(user=user_account)
    total_earnings = sum(status.earnings for status in statuses)
    images = ProductImage.objects.filter(is_active=True)
    user_history = UserHistory.objects.filter(user=user_account)

    # Update the status_form if the user has an active package
    if user_account.is_package_active():
        status_form = StatusForm()

    context = {
        'status_form': status_form,
        'package_form': package_form,
        'statuses': statuses,
        'total_earnings': total_earnings,
        'balance': account_balance,
        'user_history': user_history,
        'images': images,
        'can_upload_image': user_account.is_package_active(),
        'remaining_days': max(0, (user_account.package_expiry - timezone.now()).days) if user_account.package_expiry else 0,
        'show_add': user_account.is_package_active(),
        'active_package' : active_package
    }

    return render(request, 'whatsapp_rewards/whatsapp_status.html', context)

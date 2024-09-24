from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from refer.models import ReferralProfile, Referral

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth_app/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth_app/register.html')

        user = User.objects.create_user(username=email, email=email, password=password1)
        user.first_name = full_name.split()[0]
        if len(full_name.split()) > 1:
            user.last_name = ' '.join(full_name.split()[1:])
        user.save()

        # Handle referral
        referral_code = request.session.get('referral_code')
        if referral_code:
            try:
                referrer_profile = ReferralProfile.objects.get(referral_code=referral_code)
                Referral.objects.create(referrer=referrer_profile.user, referred_user=user)
                del request.session['referral_code']
            except ReferralProfile.DoesNotExist:
                pass  # Invalid referral code, we can ignore it

        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('auth_app:login')

    # Handle GET request
    referral_code = request.GET.get('ref')
    if referral_code:
        request.session['referral_code'] = referral_code

    return render(request, 'auth_app/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('my_profile:dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'auth_app/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('auth_app:login')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm
from django.contrib import messages
from referrals.views import complete_referral  # Import the complete_referral function

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("Form saved successfully")
            messages.success(request, 'User registered successfully!')
            
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            # Check if there's a referral code in the session
            if 'referral_code' in request.session:
                print(f"Referral code found in session: {request.session['referral_code']}")  # For debugging
                return complete_referral(request)
            else:
                print("No referral code found in session")  # For debugging
            
            return redirect('my_profile:dashboard1') # my_profile:dashboard1
    else:
        form = RegisterForm()
    return render(request, 'auth_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Check if there's a pending referral
            if 'referral_code' in request.session:
                return complete_referral(request)
            
            return redirect('my_profile:dashboard1') #my_profile:dashboard1
        else:
            return render(request, 'auth_app/login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'auth_app/login.html')
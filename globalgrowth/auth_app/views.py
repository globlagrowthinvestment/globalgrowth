from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm
from django.contrib import messages



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form saved successfully")
            messages.success(request, 'User registered successfully!')
            return redirect('auth_app:login')
    else:
        form = RegisterForm()
    return render(request, 'auth_app/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists in the database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'auth_app/login.html', {'error_message': 'Invalid username or password'})

        # Verify the password
        if user.check_password(password):
            # Authenticate the user
            auth_user = authenticate(request, username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('my_profile:dashboard1')
            else:
                return render(request, 'auth_app/login.html', {'error_message': 'Invalid username or password'})
        else:
            return render(request, 'auth_app/login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'auth_app/login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='auth_app:login')
def dashboard(request):
    # Fetch data or perform any necessary operations
    context = {
        # 'data': data,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='auth_app:login')
def invest(request):
    # Fetch data or perform any necessary operations
    context = {
        # 'data': data,
    }
    return render(request, 'my_profile/invest.html', context)

@login_required(login_url='auth_app:login')
def withdraw(request):
    # Fetch data or perform any necessary operations
    context = {
        # 'data': data,
    }
    return render(request, 'dashboard/withdraw.html', context)

@login_required(login_url='auth_app:login')
def complains(request):
    # Fetch data or perform any necessary operations
    context = {
        # 'data': data,
    }
    return render(request, 'dashboard/complains.html', context)


@login_required(login_url='auth_app:login')
def guide(request):
    #fetch data or perform any necessary operations
    context = {
        # 'data': data,
    }
    return render(request, 'dashboard/guide.html', context)


@login_required(login_url='auth_app:login')
def profile(request):
    #fetch data or perform any necessary operations
    context = {
        # 'data': data,
    }
    return render(request, 'dashboard/profile.html', context)
from django.shortcuts import render

def home(request):
    return render(request, 'landing/welcome.html')

def welcome(request):
    return render(request, 'landing/welcome.html')
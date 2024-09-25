from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Complaint
from .forms import ComplaintForm

@login_required
def complains(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('complains')
    else:
        form = ComplaintForm()

    status_filter = request.GET.get('status', '')
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    context = {
        'form': form,
        'complaints': complaints,
        'status_filter': status_filter
    }
    return render(request, 'complains/complains.html', context)
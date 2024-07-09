from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Referral
import uuid

@login_required
def referral_dashboard(request):
    # Generate or retrieve the user's referral link
    referral, created = Referral.objects.get_or_create(
        referrer=request.user,
        defaults={'referral_code': str(uuid.uuid4())[:8]}
    )
    
    referral_link = request.build_absolute_uri(reverse('referrals:track_referral', args=[referral.referral_code]))


    
    # Get all referrals made by the user
    referrals = Referral.objects.filter(referrer=request.user).select_related('referred')
    
    # Calculate total reward
    total_reward = sum(referral.reward_earned for referral in referrals)
    
    context = {
        'referral_link': referral_link,
        'referrals': referrals,
        'total_reward': total_reward,
    }
    
    return render(request, 'referrals/referrals.html', context)

def track_referral(request, referral_code):
    try:
        referral = Referral.objects.get(referral_code=referral_code)
        # Store the referral code in the session
        request.session['referral_code'] = referral_code
    except Referral.DoesNotExist:
        pass
    
    # Redirect to the signup page
    return redirect('auth_app:register')  # Make sure you have a 'signup' URL name defined

@login_required
def complete_referral(request):
    referral_code = request.session.get('referral_code')
    if referral_code:
        try:
            referral = Referral.objects.get(referral_code=referral_code)
            if referral.referrer != request.user:
                referral.referred = request.user
                referral.status = 'ACTIVE'
                referral.save()
                del request.session['referral_code']
        except Referral.DoesNotExist:
            pass
    
    return redirect('my_profile:dashboard1')  # Redirect to the user's dashboard
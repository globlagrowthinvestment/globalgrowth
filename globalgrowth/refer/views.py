from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ReferralProfile, Referral
import qrcode
from io import BytesIO
import base64

@login_required
def referral_dashboard(request):
    user_profile, created = ReferralProfile.objects.get_or_create(user=request.user)
    referrals = Referral.objects.filter(referrer=request.user)
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    referral_url = request.build_absolute_uri(f'/auth_app/register/?ref={user_profile.referral_code}')
    qr.add_data(referral_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'referral_code': user_profile.referral_code,
        'referrals': referrals,
        'qr_code': qr_image,
        'referral_url': referral_url,
    }
    return render(request, 'refer/refer.html', context)
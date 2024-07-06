import json
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
import base64
from datetime import datetime
from .models import MpesaPayment, Package  # Ensure these models are defined

def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = settings.MPESA_PASSKEY
    business_short_code = settings.MPESA_SHORTCODE
    data = f"{business_short_code}{passkey}{timestamp}"
    encoded = base64.b64encode(data.encode())
    return encoded.decode('utf-8')

def generate_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

def generate_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    r = requests.get(api_URL, auth=(consumer_key, consumer_secret))
    
    return r.json()['access_token']

@csrf_exempt
def initiate_stk_push(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        
        access_token = generate_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        request_data = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": generate_password(),
            "Timestamp": generate_timestamp(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 10,
            "PartyA": 600987,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": 254797342380,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": "Test",
            "TransactionDesc": "Payment for investment package"
        }
        
        response = requests.post(api_url, json=request_data, headers=headers)
        
        return JsonResponse(response.json())

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
@require_POST
def mpesa_callback(request):
    try:
        data = json.loads(request.body)
        
        merchant_request_id = data['Body']['stkCallback']['MerchantRequestID']
        checkout_request_id = data['Body']['stkCallback']['CheckoutRequestID']
        result_code = data['Body']['stkCallback']['ResultCode']
        result_desc = data['Body']['stkCallback']['ResultDesc']
        
        if result_code == 0:
            amount = data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
            mpesa_receipt_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
            transaction_date = data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
            phone_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
            
            payment = MpesaPayment(
                merchant_request_id=merchant_request_id,
                checkout_request_id=checkout_request_id,
                result_code=result_code,
                result_desc=result_desc,
                amount=amount,
                mpesa_receipt_number=mpesa_receipt_number,
                transaction_date=transaction_date,
                phone_number=phone_number
            )
            payment.save()
        
        else:
            # Handle failed transaction
            # Log the error or update a pending transaction
            pass
        
        return HttpResponse(status=200)
    
    except (json.JSONDecodeError, KeyError):
        return HttpResponse(status=400)

def package_list(request):
    packages = Package.objects.all()
    return render(request, 'checkout/package_list.html', {'packages': packages})
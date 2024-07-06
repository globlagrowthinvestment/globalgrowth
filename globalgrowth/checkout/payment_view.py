import requests
from django.shortcuts import render, redirect
from .models import Package

def get_access_token():
    # Safaricom Daraja API credentials
    consumer_key = 'nJ2LBFFdwW5aNftzGj1dwoBajDLqwSieiHQtXaoBKDyXWR7h'
    consumer_secret = 'Obu2axIXXE6IuwW6elUxLMwM9fKYepQOhBmEeAjg5nUAm67ELtmdLExdSUstF9pr'

    # Implement the logic to get an access token from the Safaricom Daraja API
    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    access_token = response.json().get('access_token')
    return access_token

def initiate_stk_push(access_token, amount, phone_number):
    # Safaricom Daraja API endpoint for STK Push
    stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    # STK Push request parameters
    request_data = {
        'BusinessShortCode': '174379',
        'Password': 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',
        'Timestamp': 'timestamp_in_yyyymmddhhmmss',
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': str(amount),
        'PartyA': 600982,
        'PartyB': '600000',
        'PhoneNumber': 254797342380,
        'CallBackURL': 'your_callback_url',
        'AccountReference': 'Test',
        'TransactionDesc': 'Test'
    }

    # Set the headers for the API request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Make the API request
    response = requests.post(stk_push_url, json=request_data, headers=headers)

    # Handle the response
    if response.status_code == 200:
        # Payment successful
        return response.json()
    else:
        # Payment failed
        raise Exception(f'STK Push failed with status code: {response.status_code}')

def payment_view(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        phone_number = request.POST.get('phone-number')
        package = Package.objects.get(id=package_id)

        # Initiate the STK Push
        access_token = get_access_token()
        initiate_stk_push(access_token, package.price, phone_number)

        # Redirect the user to the success page or display a success message
        return redirect('checkout:payment_success')
    else:
        packages = Package.objects.all()
        return render(request, 'checkout/package_list.html', {'packages': packages})

from django.shortcuts import redirect
from django.urls import reverse

class RedirectOnErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if there was an error (adjust this logic as needed)
        if response.status_code == 403 or response.status_code == 404:
            return redirect(reverse('auth_app:login'))

        return response

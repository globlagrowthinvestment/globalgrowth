from django.shortcuts import redirect
from django.urls import reverse

class MyProfileAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path.startswith('/profile/'):
                login_url = reverse('auth_app:login')
                return redirect(f"{login_url}?next={request.path}")
        return self.get_response(request)
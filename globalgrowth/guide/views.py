from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='auth_app:login')
def guide(request):
    #fetch data or perform any necessary operations
    context = {
        # 'data': data,
    }
    return render(request, 'dashboard/guide.html', context)

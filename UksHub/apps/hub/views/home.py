from django.shortcuts import render
from django.http.response import Http404

from UksHub.apps.hubauth.forms import SignupForm
from UksHub.apps.hubauth.views import register

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'hub/hub-base.html')
        return render(request, 'hub/home.html', {'form': SignupForm()})
    if request.method == 'POST':
        return register(request)
    raise Http404
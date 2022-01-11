from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import Http404
from UksHub.apps.hub.forms import UserProfileForm

from UksHub.apps.hubauth.forms import SignupForm
from UksHub.apps.hubauth.views import register

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'hub/hub-base.html')
        return render(request, 'hub/home.html', {'form': SignupForm()})
    if request.method == 'POST':
        return register(request)
    return Http404

@login_required
def settings_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            userpofile = form.save(commit=True)
            form = UserProfileForm(instance=userpofile)
    if request.method == 'GET':
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'hub/user-settings/settings-profile.html', {'form': form })

@login_required
def settings_keys(request):
    if request.method == 'GET':
        keys = request.user.publickey_set.all()
        return render(request, 'hub/user-settings/settings-keys.html', { 'keys': keys})
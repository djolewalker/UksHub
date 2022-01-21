from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from UksHub.apps.hub.forms import UserProfileForm

@login_required
def settings_profile(request):
    context = {}
    if request.method == 'GET':
        context['form'] = UserProfileForm(instance=request.user.userprofile)
    if request.method == 'POST':
        context['form'] = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if context['form'].is_valid():
            userpofile = context['form'].save(commit=True)
            context['form'] = UserProfileForm(instance=userpofile)
            context['notification'] = 'Profile successfullty updated!'
    return render(request, 'hub/user-settings/settings-profile.html', context )

@login_required
def settings_keys(request):
    if request.method == 'GET':
        keys = request.user.publickey_set.all()
        return render(request, 'hub/user-settings/settings-keys.html', { 'keys': keys})
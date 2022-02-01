from django.shortcuts import render
from django.http.response import Http404

from UksHub.apps.gitcore.models import Repository
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


def home_hub_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            repositories = request.user.repository_set.all()
            watched_repositories = repositories.filter()
            return render(request, 'hub/home-hub.html', {'repositories': repositories})
        return render(request, 'hub/home-hub.html', {'form': SignupForm()})
    if request.method == 'POST':
        return register(request)
    raise Http404
from django.shortcuts import render
from django.http.response import Http404

from UksHub.apps.gitcore.models import Repository
from UksHub.apps.hubauth.forms import SignupForm
from UksHub.apps.hubauth.views import register


def home_hub_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            repositories = request.user.repository_set.filter(archived=False).all()

            sorted_watched_repos_limit = request.user.repo_stars.filter(archived=False).order_by('-updated_at').all()[:5]
            sorted_starred_repos_limit = request.user.repo_watch.filter(archived=False).order_by('-updated_at').all()[:5]

            context = {
                'repositories': repositories,
                'sorted_watched_repos_limit': sorted_watched_repos_limit,
                'sorted_starred_repos_limit': sorted_starred_repos_limit,
            }
            
            return render(request, 'hub/home-hub/home-hub.html', context)
        return render(request, 'hub/home.html', {'form': SignupForm()})
    if request.method == 'POST':
        return register(request)
    raise Http404

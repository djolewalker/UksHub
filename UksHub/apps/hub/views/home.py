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
            watched_repositories = []
            for repo in repositories:
                if request.user in repo.watch.all():
                    watched_repositories.append(repo)
            sorted_watched_repos = sorted(watched_repositories, key=lambda x: x.updated_at, reverse=True)
            sorted_watched_repos_limit = sorted_watched_repos[:5]


            starred_repositories = []
            for repo in repositories:
                if request.user in repo.stars.all():
                    starred_repositories.append(repo)
            sorted_starred_repos = sorted(starred_repositories, key=lambda x: x.updated_at, reverse=True)
            sorted_starred_repos_limit = sorted_starred_repos[:5]

            context = {
                'repositories': repositories,
                'watched_repositories': watched_repositories,
                'sorted_watched_repos': sorted_watched_repos,
                'sorted_watched_repos_limit': sorted_watched_repos_limit,
                'sorted_starred_repos': sorted_starred_repos,
                'sorted_starred_repos_limit': sorted_starred_repos_limit,

            }
            return render(request, 'hub/home-hub/home-hub.html', context)
        return render(request, 'hub/home-hub/home-hub.html', {'form': SignupForm()})
    if request.method == 'POST':
        return register(request)
    raise Http404

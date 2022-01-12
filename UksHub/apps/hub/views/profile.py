from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model


def profile_overview(request, username):
    if request.method == 'GET':
        user = get_object_or_404(get_user_model(), username=username)
        tab = request.GET.get('tab')
        if tab:
            return _redirect_to_tab(request, tab, user)
        return render(request, 'hub/profile/overview.html', {'user': user, 'userprofile': user.userprofile })
    return Http404


def _redirect_to_tab(request, tab, user):
    if tab == 'repositories':
        return _repositories(request, user)
    elif tab == 'projects':
        return _projects(request, user)
    elif tab == 'packages':
        return _packages(request, user)
    elif tab == 'stars':
        return _stars(request, user)
    return Http404

def _repositories(request, user):
    return render(request, 'hub/profile/repositories.html', {'user': user, 'userprofile': user.userprofile })

def _projects(request, user):
    return render(request, 'hub/profile/projects.html', {'user': user, 'userprofile': user.userprofile })

def _packages(request, user):
    return render(request, 'hub/profile/packages.html', {'user': user, 'userprofile': user.userprofile })

def _stars(request, user):
    return render(request, 'hub/profile/stars.html', {'user': user, 'userprofile': user.userprofile })
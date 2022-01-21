from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model


def profile_overview(request, username):
    if request.method == 'GET':
        user = get_object_or_404(get_user_model(), username=username)
        tab = request.GET.get('tab')
        if request.user == user:
            repos_count = user.repository_set.filter(archived=False).count()
        else:
            repos_count = user.repository_set.filter(archived=False, private=False).count()
        context = {'user': user, 'userprofile': user.userprofile, 'repos_count': repos_count }
        if tab:
            return _redirect_to_tab(request, tab, context)
        return render(request, 'hub/profile/overview.html', context)
    raise Http404


def _redirect_to_tab(request, tab, context):
    if tab == 'repositories':
        return _repositories(request, context)
    elif tab == 'projects':
        return _projects(request, context)
    elif tab == 'packages':
        return _packages(request, context)
    elif tab == 'stars':
        return _stars(request, context)
    raise Http404

def _repositories(request, context):
    if request.user == context['user']:
        repositories = context['user'].repository_set.all()
    else:
        repositories = context['user'].repository_set.filter(private=False).all()
    return render(request, 'hub/profile/repositories.html', {**context, 'repositories': repositories})

def _projects(request, context):
    return render(request, 'hub/profile/projects.html', context)

def _packages(request, context):
    return render(request, 'hub/profile/packages.html', context)

def _stars(request, context):
    return render(request, 'hub/profile/stars.html', context)
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model

from UksHub.apps.gitcore.models import Repository

def _getRepo(requestor, username, reponame):
    user = get_object_or_404(get_user_model(), username=username)
    if user == requestor:
        return get_object_or_404(Repository, creator=user, name=reponame, archived=False)
    else:
        return get_object_or_404(Repository, creator=user, name=reponame, private=False, archived=False)


def repository(request, username, reponame):
    if request.method == 'GET':
        repository = _getRepo(request.user, username, reponame)
        return render(request, 'hub/repository/code.html', { 'repository': repository })
    return Http404


def issues(request, username, reponame):
    if request.method == 'GET':
        repository = _getRepo(request.user, username, reponame)
        return render(request, 'hub/repository/issues.html', { 'repository': repository })
    return Http404


def pull_requests(request, username, reponame):
    if request.method == 'GET':
        repository = _getRepo(request.user, username, reponame)
        return render(request, 'hub/repository/pull-requests.html', { 'repository': repository })
    return Http404


def actions(request, username, reponame):
    if request.method == 'GET':
        repository = _getRepo(request.user, username, reponame)
        return render(request, 'hub/repository/actions.html', { 'repository': repository })
    return Http404


def repository_projects(request, username, reponame):
    if request.method == 'GET':
        repository = _getRepo(request.user, username, reponame)
        return render(request, 'hub/repository/repository-projects.html', { 'repository': repository })
    return Http404


def wiki(request, username, reponame):
    if request.method == 'GET':
        repository = _getRepo(request.user, username, reponame)
        return render(request, 'hub/repository/wiki.html', { 'repository': repository })
    return Http404


def security(request, username, reponame):
    if request.method == 'GET':
        repository = _getRepo(request.user, username, reponame)
        return render(request, 'hub/repository/security.html', { 'repository': repository })
    return Http404


def insights(request, username, reponame):
    if request.method == 'GET':
        repository = _getRepo(request.user, username, reponame)
        return render(request, 'hub/repository/insights.html', { 'repository': repository })
    return Http404


def repository_settings(request, username, reponame):
    if request.method == 'GET':
        repository = _getRepo(request.user, username, reponame)
        return render(request, 'hub/repository/repository-settings.html', { 'repository': repository })
    return Http404

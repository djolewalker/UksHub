from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model

from UksHub.apps.gitcore.models import Repository
from UksHub.apps.gitcore.services import get_repository

def _find_repo(requestor, username, reponame):
    user = get_object_or_404(get_user_model(), username=username)
    if user == requestor:
        return get_object_or_404(Repository, creator=user, name=reponame, archived=False)
    else:
        return get_object_or_404(Repository, creator=user, name=reponame, private=False, archived=False)


def _get_last_commits(repo, branch):
    # https://github.com/gitpython-developers/GitPython/issues/240
    paths = [obj.path for obj in branch.commit.tree]
    commits = {}
    for commit in repo.iter_commits(branch.name, paths=paths):
        for f in commit.stats.files.keys():
            p = f[:f.index('/')] if '/' in f else f
            if p in commits:
                continue
            commits[p] = commit
        if len(commits) == len(paths):
            break
    return commits

def repository(request, username, reponame, branch=None):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        repo = get_repository(repository.creator, repository.name)
        branch = branch if branch else repository.default_branch
        branch_obj = next(filter(lambda head: head.name == branch, repo.heads), None)
        ssh_enabled = request.user.publickey_set.filter(archived=False).exists()
        
        return render(request, 'hub/repository/code.html', { 
            'repository': repository, 
            'repo': repo, 
            'branch': branch,
            'ssh_enabled': ssh_enabled,
            'branch_obj': branch_obj,
            'stats': _get_last_commits(repo, branch_obj)})
    return Http404


def issues(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/issues.html', { 'repository': repository })
    return Http404


def pull_requests(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/pull-requests.html', { 'repository': repository })
    return Http404


def actions(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/actions.html', { 'repository': repository })
    return Http404


def repository_projects(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/repository-projects.html', { 'repository': repository })
    return Http404


def wiki(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/wiki.html', { 'repository': repository })
    return Http404


def security(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/security.html', { 'repository': repository })
    return Http404


def insights(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/insights.html', { 'repository': repository })
    return Http404


def repository_settings(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/repository-settings.html', { 'repository': repository })
    return Http404

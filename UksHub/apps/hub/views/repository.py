from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from git.objects.blob import Blob

from UksHub.apps.gitcore.models import Repository
from UksHub.apps.gitcore.services import get_repository

def _find_repo(requestor, username, reponame):
    user = get_object_or_404(get_user_model(), username=username)
    if user == requestor:
        return get_object_or_404(Repository, creator=user, name=reponame, archived=False)
    else:
        return get_object_or_404(Repository, creator=user, name=reponame, private=False, archived=False)


def _get_last_commits(repo, branch, tree, nest_index):
    paths = [obj.path for obj in tree]
    commits = {}
    for commit in repo.iter_commits(branch, paths=paths):
        for f in commit.stats.files.keys():
            p = f.split('/')[nest_index] if '/' in f else f
            if p in commits:
                continue
            commits[p] = commit
        if len(commits) == len(paths):
            break
    return commits

def _find_branch_from_path(repo, path):
    all_branches = sorted([branch.name for branch in repo.branches], key=lambda x: len(x), reverse=True)
    branch = next(x for x in all_branches if path.startswith(x))
    return branch


def repository(request, username, reponame, path=None):
    if request.method == 'GET':
        repo = _find_repo(request.user, username, reponame)
        repo_obj = get_repository(repo.creator, repo.name)
        if not repo_obj: raise Http404

        ssh_enabled = request.user.publickey_set.filter(archived=False).exists()
        
        branch = _find_branch_from_path(repo_obj, path) if path else repo.default_branch
        branch_obj = next(filter(lambda head: head.name == branch, repo_obj.branches), None)
        if not branch_obj: 
            if repo_obj.heads: raise Http404
            return render(request, 'hub/repository/code.html', {'repository': repo, 'repo': repo_obj, 'ssh_enabled': ssh_enabled})

        tree = branch_obj.commit.tree
        paths = [p for p in path.replace(branch,'').split('/') if p] if path else []
        hierarchy = []
        for folder in paths:
            tree = next(filter(lambda f: f.name == folder, tree.trees), None)
            if not tree: raise Http404
            hierarchy.append({'path': tree.path, 'name': tree.name})

        return render(request, 'hub/repository/code.html', {
            'repository': repo, 
            'repo': repo_obj, 
            'branch': branch,
            'ssh_enabled': ssh_enabled,
            'tree': tree,
            'hierarchy': hierarchy,
            'commit': branch_obj.commit,
            'stats': _get_last_commits(repo_obj, branch, tree, len(paths))})
    raise Http404


def blob(request, username, reponame, path=None):
    if request.method == 'GET':
        repo = _find_repo(request.user, username, reponame)
        repo_obj = get_repository(repo.creator, repo.name)

        branch = _find_branch_from_path(repo_obj, path) if path else repo.default_branch
        branch_obj = next(filter(lambda head: head.name == branch, repo_obj.branches), None)
        if not branch_obj: 
            if repo_obj.branches: raise Http404
            return render(request, 'hub/repository/code.html', {
                'repository': repo, 
                'repo': repo_obj, 
                'ssh_enabled': request.user.publickey_set.filter(archived=False).exists() })

        blob = path.replace(f'{branch}/','')
        if not blob: raise Http404

        blob_obj = branch_obj.commit.tree[blob]
        if not blob_obj: raise Http404

        commit = next(repo_obj.iter_commits(branch, paths=blob, max_count=1), None)
        if not commit: raise Http404

        hierarchy = []
        tree = branch_obj.commit.tree
        paths = [p for p in path.replace(branch,'').split('/') if p] if path else []
        for folder in paths:
            if isinstance(tree[folder], Blob): 
                hierarchy.append({'name': blob_obj.name})
                break
            tree = next(filter(lambda f: f.name == folder, tree.trees), None)
            if not tree: raise Http404
            hierarchy.append({'path': tree.path, 'name': tree.name})

        return render(request, 'hub/repository/code.html', {
            'repository': repo, 
            'repo': repo_obj, 
            'branch': branch,
            'commit': commit,
            'blob': blob_obj,
            'hierarchy': hierarchy })
    raise Http404


def issues(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/issues.html', { 'repository': repository })
    raise Http404


def pull_requests(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/pull-requests.html', { 'repository': repository })
    raise Http404


def actions(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/actions.html', { 'repository': repository })
    raise Http404


def repository_projects(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/repository-projects.html', { 'repository': repository })
    raise Http404


def wiki(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/wiki.html', { 'repository': repository })
    raise Http404


def security(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/security.html', { 'repository': repository })
    raise Http404


def insights(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/insights.html', { 'repository': repository })
    raise Http404


def repository_settings(request, username, reponame):
    if request.method == 'GET':
        repository = _find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/repository-settings.html', { 'repository': repository })
    raise Http404

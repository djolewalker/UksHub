from django.http.response import Http404
from django.shortcuts import render

from UksHub.apps.gitcore.services import get_repository
from UksHub.apps.hub.services import find_branch_from_path, find_repo, generate_hierarchy, get_last_commits, is_user_ssh_enabled


def tree(request, username, reponame, path=None):
    if request.method == 'GET':
        repo = find_repo(request.user, username, reponame)
        repo_obj = get_repository(repo.creator, repo.name)
        if not repo_obj:
            raise Http404

        ssh_enabled = is_user_ssh_enabled(request.user)

        branch = find_branch_from_path(
            repo_obj, path) if path else repo.default_branch
        branch_obj = next(filter(lambda head: head.name ==
                          branch, repo_obj.branches), None)
        if not branch_obj:
            if repo_obj.heads:
                raise Http404
            return render(request, 'hub/repository/code.html', {
                'repository': repo,
                'repo': repo_obj,
                'ssh_enabled': ssh_enabled})

        path_sections_count = sum([1 for p in path.replace(branch, '')
                                   .split('/') if p]) if path else 0
        hierarchy, tree = generate_hierarchy(branch_obj, path)

        return render(request, 'hub/repository/code.html', {
            'repository': repo,
            'repo': repo_obj,
            'branch': branch,
            'ssh_enabled': ssh_enabled,
            'tree': tree,
            'hierarchy': hierarchy,
            'commit': branch_obj.commit,
            'stats': get_last_commits(repo_obj, branch, tree, path_sections_count)})
    raise Http404


def blob(request, username, reponame, path=None):
    if request.method == 'GET':
        repo = find_repo(request.user, username, reponame)
        repo_obj = get_repository(repo.creator, repo.name)

        branch = find_branch_from_path(
            repo_obj, path) if path else repo.default_branch
        branch_obj = next(filter(lambda head: head.name ==
                          branch, repo_obj.branches), None)
        if not branch_obj:
            if repo_obj.branches:
                raise Http404
            return render(request, 'hub/repository/code.html', {
                'repository': repo,
                'repo': repo_obj,
                'ssh_enabled': is_user_ssh_enabled(request.user)})

        blob = path.replace(f'{branch}/', '')
        if not blob:
            raise Http404

        blob_obj = branch_obj.commit.tree[blob]
        if not blob_obj:
            raise Http404

        commit = next(repo_obj.iter_commits(
            branch, paths=blob, max_count=1), None)
        if not commit:
            raise Http404

        return render(request, 'hub/repository/code.html', {
            'repository': repo,
            'repo': repo_obj,
            'branch': branch,
            'commit': commit,
            'blob': blob_obj,
            'hierarchy': generate_hierarchy(branch_obj, path)[0]})
    raise Http404


def issues(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/issues.html', {'repository': repository})
    raise Http404


def pull_requests(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/pull-requests.html', {'repository': repository})
    raise Http404


def actions(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/actions.html', {'repository': repository})
    raise Http404


def repository_projects(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/repository-projects.html', {'repository': repository})
    raise Http404


def wiki(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/wiki.html', {'repository': repository})
    raise Http404


def security(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/security.html', {'repository': repository})
    raise Http404


def insights(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/insights.html', {'repository': repository})
    raise Http404


def repository_settings(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        return render(request, 'hub/repository/repository-settings.html', {'repository': repository})
    raise Http404

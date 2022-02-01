from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from git.objects.blob import Blob
from django.contrib.auth import get_user_model
from UksHub.apps.gitcore.models import Repository


def find_repo(requestor, username, reponame):
    user = get_object_or_404(get_user_model(), username=username)
    if user == requestor:
        return get_object_or_404(Repository, creator=user, name=reponame)
    else:
        repo = get_object_or_404(
            Repository, creator=user, name=reponame, archived=False)
        if repo.private:
            if requestor not in repo.contributors:
                raise PermissionDenied()
        return repo


def get_last_commits(repo, branch, tree, nest_index):
    paths = [obj.path for obj in tree]
    commits = {}
    splits = 0
    deletes = 0

    for commit in repo.iter_commits(branch, paths=paths):
        for f in commit.stats.files.keys():
            for i in f.split(' => '):
                p = i.split('/')[nest_index] if '/' in i else i
                if p in commits:
                    continue
                if p not in paths:
                    deletes += 1
                commits[p] = commit
            splits += len(f.split(' => ')) - 1 + deletes
        if len(commits) == len(paths) + splits:
            break

    return commits


def find_branch_from_path(repo, path):
    all_branches = sorted(
        [branch.name for branch in repo.branches], key=lambda x: len(x), reverse=True)
    branch = next(x for x in all_branches if path.startswith(x))
    return branch


def is_user_ssh_enabled(user):
    return user.is_authenticated and user.publickey_set.filter(archived=False).exists()


def generate_hierarchy(branch, path):
    tree = branch.commit.tree
    paths = [p for p in path.replace(
        branch.name, '').split('/') if p] if path else []
    hierarchy = []
    for entity in paths:
        if isinstance(tree[entity], Blob):
            hierarchy.append({'name': tree[entity].name})
            break
        tree = next(filter(lambda f: f.name == entity, tree.trees), None)
        if not tree:
            raise Http404
        hierarchy.append({'path': tree.path, 'name': tree.name})
    return hierarchy, tree


def can_modify_repo(user, repository):
    if not user or not repository:
        raise Http404
    if repository.creator != user and not repository.contributors.filter(pk=user.id).exists():
        raise PermissionDenied()


def can_delete_repo(user, repository):
    if not user or not repository:
        raise Http404
    if repository.creator != user:
        raise PermissionDenied()

from os import path, makedirs, rmdir
import subprocess
from git import Repo
from django.conf import settings
from django.template.loader import render_to_string

from .decorators import clone_or_pull_admin

@clone_or_pull_admin
def init_repository(repo):
    repo_name = f'{repo.creator.username}/{repo.name}'
    with open(settings.GIT_ADMIN_CONF, 'r+') as conf_file:
        include_stmt = f'include "{repo_name}.conf"'
        for line in conf_file:
            if include_stmt in line:
                break
        else:
            conf_file.write('\n')
            conf_file.write(include_stmt)
    repo_config_dir = path.join(settings.GIT_ADMIN_CONF_REPO, repo.creator.username)
    if not path.exists(repo_config_dir):
        makedirs(repo_config_dir)
    _sync_repo(repo)
    push_admin_changes(f'{repo_name} repo created')


@clone_or_pull_admin
def sync_repo(repo):
    _sync_repo(repo)
    push_admin_changes(f'{repo.name} repo synchronized')

@clone_or_pull_admin
def sync_user_keys(user):
    keys = user.publickey_set.all()
    changes = 0
    for key in keys:
        keyPath = ''
        if key.label:
            keyPath = path.join(settings.GIT_ADMIN_KEYS, key.label, f'{user.username}.pub')
        else:
            keyPath = path.join(settings.GIT_ADMIN_KEYS, f'{user.username}.pub')
        if key.archived:
            if path.exists(keyPath):
                changes+=1
                rmdir(keyPath)
        else:
            changes+=1
            if not path.exists(path.dirname(keyPath)):
                makedirs(path.dirname(keyPath))
            with open(keyPath, 'w') as key_file:
                key_file.write(key.public_key)
    if changes > 0:
        push_admin_changes(f'{user.username}\'s keys synchronized')

def _sync_repo(repo):
    repo_config = path.join(settings.GIT_ADMIN_CONF_REPO, repo.creator.username, repo.name + '.conf')
    contributors = repo.contributors.all()
    with open(repo_config, 'w') as repo_conf_file:
        repo_conf_file.write(render_to_string('repo_conf.conf', 
                                    { 
                                        'repo': repo, 
                                        'superuser': settings.GIT_ADMIN_SUPERUSER,
                                        'contributors': contributors
                                    }))

def get_repository(user,name):
    repoPath = path.join(settings.GIT_REPOSITORIES, user.username, f'{name}.git')
    try:
        repo = Repo(repoPath)
    except:
        repo = None
    return repo

def push_admin_changes(message):
    subprocess.call(['git', 'add', '*'], cwd=settings.GIT_ADMIN)
    subprocess.call(['git', 'commit','-m', f'"{message}"'], cwd=settings.GIT_ADMIN)
    subprocess.call(['git', 'push'], cwd=settings.GIT_ADMIN)
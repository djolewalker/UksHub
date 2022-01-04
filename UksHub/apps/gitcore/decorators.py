from os import path, getcwd
from django.conf import settings
import subprocess

def clone_or_pull_admin(func):
    def pull(*args, **kwargs):
        print(getcwd())
        if not path.exists(settings.GIT_ADMIN):
            subprocess.call(['git', 'clone', settings.GIT_ADMIN_REMOTE])
        subprocess.call(['git', 'pull'], cwd=settings.GIT_ADMIN)
        func(*args, **kwargs)
    return pull
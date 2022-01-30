from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings

from .models import Repository, PublicKey
from .services import init_repository, init_repository_dev, sync_repo, sync_user_keys
from .forms import KeyForm, RepositoryForm, RepositoryContributorsForm


@login_required
def init_repo(request):
    if request.method == 'POST':
        repo_form = RepositoryForm(request.POST, initial={
                                   'isPublic': True, 'owner': request.user.username})
        if repo_form.is_valid():
            try:
                repo = repo_form.save(commit=False)
                repo.creator = request.user
                repo.private = not repo_form.cleaned_data['isPublic']
                repo.save()
                repo.contributors.add(repo.creator)
                if settings.USE_DEV_GIT:
                    init_repository_dev(repo)
                else:
                    init_repository(repo)
                return redirect(f'/{request.user.username}?tab=repositories')
            except IntegrityError:
                repo_form.add_error(
                    'name', 'You have already created repository with this name!')
    if request.method == 'GET':
        repo_form = RepositoryForm(
            initial={'isPublic': True, 'owner': request.user.username})
    else:
        raise Http404
    return render(request, 'git-core/create-repo.html', {'form': repo_form}) if repo_form else HttpResponse(status=409)


# TODO: just a test, should be integrated in HUB
@login_required
def add_contributor(request, repoId):
    if request.method == 'POST':
        repo = get_object_or_404(Repository, pk=repoId)
        contr_form = RepositoryContributorsForm(
            repo.creator, request.POST, instance=repo)
        if contr_form.is_valid():
            repo = contr_form.save()
            repo.contributors.add(repo.creator)
            sync_repo(repo)
            return HttpResponse(status=200)
    elif request.method == 'GET':
        repo = get_object_or_404(Repository, pk=repoId)
        contr_form = RepositoryContributorsForm(repo.creator, instance=repo)
    else:
        raise Http404
    return render(request, 'git-core/create-form.html', {'form': contr_form}) if contr_form else Http404


@login_required
def public_key(request):
    note = None
    if request.method == 'POST':
        key_form = KeyForm(request.POST)
        if key_form.is_valid():
            try:
                if PublicKey.objects.filter(owner=request.user, label=None).exists():
                    PublicKey.objects.filter(
                        owner=request.user, label=None).delete()
                key = key_form.save(commit=False)
                key.owner = request.user
                key.save()
                sync_user_keys(request.user)
                return redirect('settings-keys')
            except IntegrityError:
                key_form.add_error(
                    'label', 'Only one key can be labeled with same label!')
    if request.method == 'GET':
        if PublicKey.objects.filter(owner=request.user, label=None).exists():
            note = 'You have set unlabeled public key. Create new one with specified label. Otherwise current unlabeled public key will be overridden!'
        key_form = KeyForm()
    else:
        raise Http404
    return render(request, 'hub/user-settings/settings-new-ssh.html', {'form': key_form, 'note': note}) if key_form else Http404

from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .models import Repository, PublicKey
from .services import init_repository, sync_repo, sync_user_keys
from .forms import KeyForm, RepositoryForm, RepositoryContributorsForm


@login_required
def init_repo(request):
    if request.method == 'POST':
        repo_form = RepositoryForm(request.POST)
        if repo_form.is_valid():
            repo = repo_form.save()
            repo.creator = request.user
            repo.save()
            init_repository(repo)
            return HttpResponse(status=200)
    if request.method == 'GET':
        repo_form = RepositoryForm()
    return render(request, 'hub/git-core/create-form.html', {'form': repo_form }) if repo_form  else HttpResponse(status=409)

@login_required
def add_contributor(request, repoId):
    if request.method == 'POST':
        repo = get_object_or_404(Repository, pk=repoId)
        contr_form = RepositoryContributorsForm(repo.creator, request.POST, instance=repo)
        if contr_form.is_valid():
            repo = contr_form.save()
            sync_repo(repo)
            return HttpResponse(status=200)
    if request.method == 'GET':
        repo = get_object_or_404(Repository, pk=repoId)
        contr_form = RepositoryContributorsForm(repo.creator, instance=repo)
    return render(request, 'hub/git-core/create-form.html', {'form': contr_form }) if contr_form else Http404

@login_required
def set_public_key(request):
    note = None
    if request.method == 'POST':
        key_form = KeyForm(request.POST)
        if key_form.is_valid():
            try:
                key = key_form.save(commit=False)
                key.owner = request.user
                key.save()
                sync_user_keys(request.user)
                return HttpResponse(status=200)
            except IntegrityError:
                key_form.add_error('label', 'Only one key can be labeled with same label!')
    if request.method == 'GET':
        if PublicKey.objects.filter(owner=request.user, label=None).exists():
            note = 'You have set unlabeled public key. Create new one with specified label. Otherwise current unlabeled public key will be overridden!' 
        key_form = KeyForm()
    return render(request, 'hub/git-core/create-form.html', { 'form': key_form, 'note': note }) if key_form else Http404
        
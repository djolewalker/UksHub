import binascii
import math
from django.db.models.functions import TruncDay
from django.db.models import Count
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from base64 import b64decode
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from UksHub.apps.analytics.models import Visit
from UksHub.apps.core.constants import EMPTY_TREE_SHA
from UksHub.apps.core.enums import BASE_STATE
from UksHub.apps.events.forms import CommentForm
from UksHub.apps.gitcore.forms import RepositoryContributorsForm
from UksHub.apps.gitcore.models import Commit, Repository
from UksHub.apps.events.services import event_artefact_state_change, event_user_to_artefact
from UksHub.apps.gitcore.services import can_merge, get_repository, merge, sync_repo
from UksHub.apps.hub.forms import IssueForm, PullRequestForm
from UksHub.apps.hub.services import can_delete_repo, can_modify_repo, find_branch_from_path, find_repo, generate_hierarchy, get_last_commits, is_user_ssh_enabled
from UksHub.apps.advancedsearch.models import Query
from UksHub.apps.advancedsearch.mapper import get_artefact_content_type, map_query_to_filter


_sort_options = [
    ('sort:created-desc', 'Newest'),
    ('sort:created-asc', 'Oldest'),
    ('sort:comments-desc', 'Most commented'),
    ('sort:comments-asc', 'Least commented'),
    ('sort:updated-desc', 'Recently updated'),
    ('sort:updated-asc', 'Least recently updated')
]


def _execute_query(repository, query):
    if query:
        f, s, e, a, m, q = map_query_to_filter(query)

        artefacts = repository.artefact_set.annotate(
            **a
        ).filter(
            *m,
            **f,
        ).exclude(
            **e
        ).order_by(
            *s
        ).all()

    else:
        artefacts = repository.artefact_set.all()
        q = Query()

    queries = {
        'open': q.set_state('is:open'),
        'closed': q.set_state('is:closed'),
        'author': q.clear_author(),
        'assignee': q.clear_assignee(),
        'sort': q.clear_sort()
    }

    return artefacts, q, queries


def _create_artefact_from_form(requestor, repository, form, comment_form):
    if form.is_valid():
        artefact = form.save(commit=False)
        artefact.repository = repository
        artefact.creator = requestor
        artefact.save()
        form.save_m2m()

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = requestor
            comment.artefact = artefact
            comment.save()
            artefact.message = comment
            artefact.save()

        # Create events
        if artefact.assignees.all():
            event_user_to_artefact(
                requestor, artefact, artefact.assignees.all()
            )
        return artefact
    return None


def _generate_stats(commits):
    stats = {
        'files': {},
        'total': {'files': 0, 'insertions': 0, 'deletions': 0}
    }
    for commit in commits:
        stats['total']['insertions'] += commit.stats.total['insertions']
        stats['total']['deletions'] += commit.stats.total['deletions']
        for file in commit.stats.files.keys():
            if file not in stats['files']:
                stats['total']['files'] += 1
                stats['files'][file] = {'insertions': 0, 'deletions': 0}
            stats['files'][file]['insertions'] += commit.stats.files[file]['insertions']
            stats['files'][file]['deletions'] += commit.stats.files[file]['deletions']
    return stats


def _get_compare_context(repo, comparation, pr=None, comment=None):
    repo_obj = get_repository(repo.creator, repo.name)

    if comparation != None and '...' not in comparation:
        raise Http404

    base, comparator = comparation.split('...') if comparation else (
        repo.default_branch, repo.default_branch)

    context = {
        'repository': repo,
        'repo': repo_obj,
        'base': base,
        'comparator': comparator
    }

    if repo_obj.branches:
        base_br = find_branch_from_path(repo_obj, base)
        comparator_br = find_branch_from_path(repo_obj, comparator)

        if not base_br or not comparator_br:
            raise Http404

        if base_br != comparator_br:

            base_obj = next(filter(lambda head: head.name ==
                                   base_br, repo_obj.branches), None)
            comparator_obj = next(filter(lambda head: head.name ==
                                         comparator_br, repo_obj.branches), None)

            if comparator_obj.commit in [base_obj.commit, *base_obj.commit.iter_parents()]:
                context['is_child'] = True
            else:
                commits = [comparator_obj.commit]
                for cmt in comparator_obj.commit.iter_parents():
                    if cmt == base_obj.commit:
                        break
                    commits.append(cmt)

                diffs = base_obj.commit.diff(
                    comparator_obj.commit, create_patch=True)
                splitted = [i.diff.decode().splitlines() for i in diffs]

                if pr:
                    pr_form = PullRequestForm(pr)
                else:
                    pr_form = PullRequestForm()
                    pr_form.fields['assignees'].queryset = repo.contributors

                if not pr or not pr.is_merged:
                    context['can_merge'] = can_merge(
                        repo, repo_obj, base, comparator)

                context['artefact_form'] = pr_form
                context['comment_form'] = CommentForm(
                    comment) if comment else CommentForm()
                context['diffs'] = diffs
                context['splitted'] = splitted
                context['stats'] = _generate_stats(commits)
                context['commits'] = commits
        else:
            context['is_same'] = True
    else:
        context['is_empty'] = True
    return context


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


def commits(request, username, reponame, branch=None):
    if request.method == 'GET':
        repo = find_repo(request.user, username, reponame)
        repo_obj = get_repository(repo.creator, repo.name)
        branch_name = find_branch_from_path(
            repo_obj, branch) if branch else repo.default_branch
        commits = list(repo_obj.iter_commits(branch_name))

        return render(request, 'hub/repository/commits.html', {
            'repository': repo,
            'repo': repo_obj,
            'branch': branch_name,
            'commits': commits
        })

    raise Http404


def commit(request, username, reponame, commit):
    if request.method == 'GET':
        repo = find_repo(request.user, username, reponame)
        repo_obj = get_repository(repo.creator, repo.name)
        commit = Commit(repo_obj, b64decode(commit.encode()))

        parent = commit.parents[0] if commit.parents else Commit(
            repo_obj, binascii.unhexlify(EMPTY_TREE_SHA))

        diffs = parent.diff(commit, paths=list(
            commit.stats.files.keys()), create_patch=True)
        splitted = [i.diff.decode().splitlines() for i in diffs]

        return render(request, 'hub/repository/commit.html', {
            'repository': repo,
            'commit': commit,
            'diffs': diffs,
            'splitted': splitted,
            'stats': commit.stats
        })

    raise Http404


def issues(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        default_query = 'is:issue is:open'
        query = request.GET.get('q', default_query)
        artefacts, return_query, binding_queries = _execute_query(
            repository,
            query
        )

        return render(request, 'hub/repository/artefacts.html', {
            'repository': repository,
            'artefacts': artefacts,
            'query': str(return_query),
            'queries': binding_queries,
            'ispr': False,
            'is_default_query': query == default_query,
            'sort_options': _sort_options
        })

    raise Http404


def issue(request, username, reponame, id):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        issue = repository.artefact_set.get(pk=id)
        if not issue:
            raise Http404
        return render(request, 'hub/repository/issue.html', {'repository': repository, 'issue': issue})
    raise Http404


@login_required
def close_issue(request, username, reponame, id):
    if request.method == 'POST':
        repo = find_repo(request.user, username, reponame)
        pr = repo.artefact_set.get(pk=id)
        if not pr:
            raise Http404
        pr.state = BASE_STATE.CLOSED.value
        pr.save()
        event_artefact_state_change(request.user, pr, pr.state)
        return redirect(reverse('issue', kwargs={'username': username, 'reponame': reponame, 'id': pr.id}))
    else:
        raise Http404


@login_required
def create_issue(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        can_modify_repo(request.user, repository)
        issue_form = IssueForm()
        issue_form.fields['assignees'].queryset = repository.contributors
        comment_form = CommentForm()

    elif request.method == 'POST':
        repository = find_repo(request.user, username, reponame)
        can_modify_repo(request.user, repository)
        issue_form = IssueForm(request.POST)
        comment_form = CommentForm(request.POST)
        issue = _create_artefact_from_form(
            request.user, repository, issue_form, comment_form)
        if issue:
            return redirect(reverse('issue', kwargs={'username': username, 'reponame': reponame, 'id': issue.id}))
    else:
        raise Http404
    return render(request, 'hub/repository/new-issue.html', {'repository': repository, 'artefact_form': issue_form, 'comment_form': comment_form})


def pull_requests(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        default_query = 'is:pr is:open'
        query = request.GET.get('q', default_query)
        artefacts, return_query, binding_queries = _execute_query(
            repository,
            query
        )

        return render(request, 'hub/repository/artefacts.html', {
            'repository': repository,
            'artefacts': artefacts,
            'query': str(return_query),
            'queries': binding_queries,
            'ispr': True,
            'is_default_query': query == default_query,
            'sort_options': _sort_options
        })

    raise Http404


@login_required
def compare(request, username, reponame, comparation=None):
    if request.method == 'GET':
        repo = find_repo(request.user, username, reponame)
        can_modify_repo(request.user, repo)
        context = _get_compare_context(repo, comparation)
    elif request.method == 'POST':
        repo = find_repo(request.user, username, reponame)
        can_modify_repo(request.user, repo)
        pr_form = PullRequestForm(request.POST)
        comment_form = CommentForm(request.POST)
        pr = _create_artefact_from_form(
            request.user, repo, pr_form, comment_form)
        context = _get_compare_context(repo, comparation, pr, comment_form)
        if pr:
            pr.source = context['comparator']
            pr.target = context['base']
            pr.save()
            return redirect(reverse('pull-request', kwargs={'username': username, 'reponame': reponame, 'id': pr.id}))
    else:
        raise Http404
    return render(request, 'hub/repository/compare.html', context)


def pull_request(request, username, reponame, id):
    if request.method == 'GET':
        repo = find_repo(request.user, username, reponame)
        pr = repo.artefact_set.get(pk=id)
        if not pr:
            raise Http404
        context = _get_compare_context(
            repo, '...'.join([pr.target, pr.source]), pr)
        context['pr'] = pr

    elif request.method == 'POST':
        repo = find_repo(request.user, username, reponame)
        can_modify_repo(request.user, repo)
        pr = repo.artefact_set.get(pk=id)
        if not pr:
            raise Http404
        context = _get_compare_context(
            repo, '...'.join([pr.target, pr.source]), pr)
        merge_status = merge(repo, context['repo'], pr.target, pr.source)
        if merge_status:
            pr.state = BASE_STATE.CLOSED.value
            pr.is_merged = True
            pr.save()
            context['pr'] = pr
        else:
            context['error'] = 'Something went wrong. Pull request can\'t be merged!'
    else:
        raise Http404
    return render(request, 'hub/repository/pull-request.html', context)


@login_required
def close_pull_request(request, username, reponame, id):
    if request.method == 'POST':
        repo = find_repo(request.user, username, reponame)
        can_modify_repo(request.user, repo)
        pr = repo.artefact_set.get(pk=id)
        if not pr:
            raise Http404
        pr.state = BASE_STATE.CLOSED.value
        pr.save()
        event_artefact_state_change(request.user, pr, pr.state)
        return redirect(reverse('pull-request', kwargs={'username': username, 'reponame': reponame, 'id': pr.id}))
    else:
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


def pulse(request, username, reponame, period='weekly'):
    if request.method == 'GET':
        today = timezone.localdate()
        if period == 'daily':
            after_day = today - timedelta(days=1)
        elif period == 'weekly':
            after_day = today - timedelta(days=7)
        elif period == 'monthly':
            after_day = today - timedelta(days=30)
        else:
            raise Http404

        repo = find_repo(request.user, username, reponame)
        repo_obj = get_repository(repo.creator, repo.name)
        if not repo_obj:
            raise Http404

        issues = repo.artefact_set.filter(Q(created_at__gte=after_day) | Q(
            updated_at__gte=after_day), polymorphic_ctype=get_artefact_content_type('issue')).all()
        prs = repo.artefact_set.filter(Q(created_at__gte=after_day) | Q(
            updated_at__gte=after_day), polymorphic_ctype=get_artefact_content_type('pr')).all()

        issues_open = sum(x.state == BASE_STATE.OPEN.value for x in issues)
        issues_close = sum(x.state == BASE_STATE.CLOSED.value for x in issues)
        prs_open = sum(x.state == BASE_STATE.OPEN.value for x in prs)
        prs_close = sum(x.state == BASE_STATE.CLOSED.value for x in prs)

        authors = list()
        commits = 0
        files = list()
        additions = 0
        deletions = 0
        for commit in repo_obj.iter_commits(repo.default_branch):
            if commit.committed_datetime.date() < after_day:
                break
            if commit.author not in authors:
                authors.append(commit.author)
            commits += 1
            files = [*files, *list(commit.stats.files.keys())]
            additions += commit.stats.total['insertions']
            deletions -= commit.stats.total['deletions']

        return render(request, 'hub/repository/insights/pulse.html', {
            'repository': repo,
            'period': period,
            'issues_open': issues_open,
            'issues_close': issues_close,
            'pr_open': prs_open,
            'prs_close': prs_close,
            'authors': len(authors),
            'commits': commits,
            'files': len(files),
            'additions': additions,
            'deletions': deletions
        })
    raise Http404


def insights_commits(request, username, reponame):
    if request.method == 'GET':
        repo = find_repo(request.user, username, reponame)
        repo_obj = get_repository(repo.creator, repo.name)
        if not repo_obj:
            raise Http404

        today = timezone.localdate()
        dates = list()
        total_day_dif = (today - repo.created_at.date()).days
        slices = 5 if total_day_dif >= 5 else total_day_dif
        if total_day_dif < 5:
            increment = 1
        else:
            increment = total_day_dif / 5

        for x in range(slices):
            dates.append({
                'date': repo.created_at.date() + timedelta(days=math.ceil(increment*(x+1))),
                'count': 0
            })

        user_stats = list()
        selected_dates = [i['date'] for i in dates]
        cmt_count = 0
        for commit in repo_obj.iter_commits(repo.default_branch):
            cmt_count += 1
            cmt_date = commit.committed_datetime.date()
            for index, d in enumerate(selected_dates):
                if cmt_date <= d:
                    dates[index]['count'] += 1
                    break
            current_user = next(filter(
                lambda u: u['user']['userprofile']['email'] == commit.author.email, user_stats), None)
            if current_user:
                current_user['stats']['commits'] += 1
                current_user['stats']['insertions'] += commit.stats.total['insertions']
                current_user['stats']['deletions'] += commit.stats.total['deletions']
            elif get_user_model().objects.filter(email=commit.author.email).exists():
                user_stats.append({
                    'user': get_user_model().objects.get(email=commit.author.email),
                    'stats': {'commits': 0, 'insertions': 0, 'deletions': 0}
                })
            else:
                user_stats.append({
                    'user': {'unknown': True, 'userprofile': {'username': commit.author.name, 'email': commit.author.email}},
                    'stats': {'commits': 0, 'insertions': 0, 'deletions': 0}
                })

        return render(request, 'hub/repository/insights/commits.html', {
            'repository': repo,
            'today': today,
            'data': dates if cmt_count else None,
            'user_stats': sorted(user_stats, key=lambda x: x['stats']['commits'])
        })
    raise Http404


def insights_trafic(request, username, reponame):
    if request.method == 'GET':
        repo = find_repo(request.user, username, reponame)
        repo_obj = get_repository(repo.creator, repo.name)
        if not repo_obj:
            raise Http404

        today = timezone.localdate()
        dates = list()
        for i in range(14):
            dates.append({
                'date': today - timedelta(days=i),
                'visits': 0,
                'visitors': 0
            })

        visits = Visit.objects.filter(
            time__gte=dates[13]['date'],
            path__startswith=f"/{username}/{reponame}"
        ).annotate(
            day=TruncDay('time')
        ).values(
            'day'
        ).annotate(
            visits=Count('id')
        ).values(
            'day', 'visits'
        ).annotate(
            unique=Count('session_id', distinct=True)
        ).values(
            'day', 'visits', 'unique'
        ).order_by(
            '-day'
        ).all()
        
        for visit_date in list(visits):
            for store_date in dates:
                if store_date['date'] == visit_date['day'].date():
                    store_date['visits'] = visit_date['visits']
                    store_date['visitors'] = visit_date['unique']

        return render(request, 'hub/repository/insights/traffic.html', {
            'repository': repo,
            'data': sorted(dates, key=lambda x: x['date'])
        })
    raise Http404


@login_required
def repository_settings(request, username, reponame):
    if request.method == 'GET':
        repository = find_repo(request.user, username, reponame)
        can_modify_repo(request.user, repository)
        print(repository.private)
        return render(request, 'hub/repository/settings/repo-main-settings.html', {'repository': repository})
    raise Http404


@login_required
def change_private_status(request, pk):
    if request.method == 'POST':
        repo = get_object_or_404(Repository, id=pk)
        can_delete_repo(request.user, repo)

        repo.private = not repo.private
        repo.save()

        return redirect(request.GET['next'])
    else:
        raise Http404


@login_required
def archive_repo(request, pk):
    if request.method == 'POST':
        repo = get_object_or_404(Repository, id=pk)
        can_delete_repo(request.user, repo)

        repo.archived = not repo.archived
        repo.save()

        return redirect(request.GET['next'])
    else:
        raise Http404


@login_required
def delete_repo(request, pk):
    if request.method == 'POST':
        repo = get_object_or_404(Repository, id=pk)
        can_delete_repo(request.user, repo)

        repo.delete()

        return redirect(request.GET['next'])
    else:
        raise Http404


@login_required
def collaborators(request, username, reponame):
    if request.method == 'GET':
        repo = find_repo(request.user, username, reponame)
        can_modify_repo(request.user, repo)
        contr_form = RepositoryContributorsForm(repo.creator, instance=repo)
    elif request.method == 'POST':
        repo = find_repo(request.user, username, reponame)
        can_modify_repo(request.user, repo)
        contr_form = RepositoryContributorsForm(
            repo.creator, request.POST, instance=repo)
        if contr_form.is_valid():
            repo = contr_form.save()
            repo.contributors.add(repo.creator)
            sync_repo(repo)
    else:
        raise Http404
    return render(request, 'hub/repository/settings/collaborators.html', {'repository': repo, "form": contr_form})


@login_required
def star_view(request, pk):
    if request.method == 'POST':
        repo = get_object_or_404(Repository, id=pk)

        if request.user in repo.stars.all():
            repo.stars.remove(request.user)
        else:
            repo.stars.add(request.user)

        return redirect(request.GET['next'])
    else:
        raise Http404


@login_required
def watch_view(request, pk):
    if request.method == 'POST':
        repo = get_object_or_404(Repository, id=pk)
        if request.user in repo.watch.all():
            repo.watch.remove(request.user)
        else:
            repo.watch.add(request.user)
        return redirect(request.GET['next'])
    else:
        raise Http404

from django.urls import path
from django.views.generic import RedirectView

from .views.home import home_hub_view
from .views.profile import profile_overview
from .views.profile_settings import settings_keys, settings_profile

from .views.repository import actions, archive_repo, blob, change_private_status, close_issue, close_pull_request, \
    collaborators, commit, commits, compare, create_issue, delete_repo, insights, issue, issues, pull_request, \
    pull_requests, tree, repository_projects, repository_settings, security, wiki, star_view, watch_view, \
    create_milestone, milestones, milestone

urlpatterns = [
    # Home
    path('', home_hub_view, name='home'),
    # User profile
    path('<username>', profile_overview, name='profile'),
    # User profile settings
    path('settings', RedirectView.as_view(url='settings/profile', permanent=False)),
    path('settings/profile', settings_profile, name='settings-profile'),
    path('settings/keys', settings_keys, name='settings-keys'),

    
    # Repository

    path('star/<int:pk>', star_view, name = 'star_repo'),
    path('watch/<int:pk>', watch_view, name = 'watch_repo'),
    path('repo-settings/delete/<int:pk>', delete_repo, name='delete-repository'),
    path('repo-settings/archive/<int:pk>', archive_repo, name='archive-repository'),
    path('repo-settings/private_status/<int:pk>', change_private_status, name='repository-private-status'),
    path('<username>/<reponame>', tree, name='repository'),
    path('<username>/<reponame>/milestones', milestones, name='milestones'),
    path('<username>/<reponame>/new-milestone', create_milestone, name='new-milestone'),
    path('<username>/<reponame>/milestones/<int:id>', milestone, name='milestone'),
    path('<username>/<reponame>/tree/<path:path>', tree, name='repository-tree'),
    path('<username>/<reponame>/blob/<path:path>', blob, name='repository-blob'),
    path('<username>/<reponame>/commits', commits, name='commits'),
    path('<username>/<reponame>/commits/<path:branch>', commits, name='branch-commits'),
    path('<username>/<reponame>/commit/<path:commit>', commit, name='commit'),
    path('<username>/<reponame>/issues', issues, name='issues'),
    path('<username>/<reponame>/issues/<int:id>', issue, name='issue'),
    path('<username>/<reponame>/issues/<int:id>/close', close_issue, name='close-issue'),
    path('<username>/<reponame>/issues/new', create_issue, name='create-issue'),
    path('<username>/<reponame>/pulls', pull_requests, name='pull-requests'),
    path('<username>/<reponame>/pulls/<int:id>', pull_request, name='pull-request'),
    path('<username>/<reponame>/pulls/<int:id>/close', close_pull_request, name='close-pull-request'),
    path('<username>/<reponame>/compare', compare, name='compare'),
    path('<username>/<reponame>/compare/<path:comparation>', compare, name='compare-branches'),
    path('<username>/<reponame>/actions', actions, name='actions'),
    path('<username>/<reponame>/projects', repository_projects, name='repository-projects'),
    path('<username>/<reponame>/wiki', wiki, name='wiki'),
    path('<username>/<reponame>/security', security, name='security'),
    path('<username>/<reponame>/insights', insights, name='insights'),
    path('<username>/<reponame>/settings', repository_settings, name='repository-settings'),
    path('<username>/<reponame>/settings/collaborators', collaborators, name='repository-collaborators'),
]

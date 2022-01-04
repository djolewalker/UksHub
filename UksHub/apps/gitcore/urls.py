from django.urls.conf import path

from UksHub.apps.gitcore.views import add_contributor, init_repo, set_public_key

urlpatterns = [
    path('new', init_repo, name='new-repo'),
    path('add-cotributor/<int:repoId>/', add_contributor, name='set-contributor'),
    path('create-public-key', set_public_key, name='create-public-key')
]
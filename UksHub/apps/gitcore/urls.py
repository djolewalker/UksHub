from django.urls.conf import path

from .views import add_contributor, init_repo, public_key

urlpatterns = [
    path('new', init_repo, name='new-repo'),
    path('settings/keys/new-ssh', public_key, name='settings-keys-new'),
]
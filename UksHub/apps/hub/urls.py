from django.urls import path
from django.views.generic import RedirectView

from .views.home import home
from .views.profile import profile_overview
from .views.profile_settings import settings_keys, settings_profile

urlpatterns = [
    # Home
    path('', home, name='home'),
    # User profile
    path('<username>', profile_overview, name='profile'),
    # User profile settings
    path('settings', RedirectView.as_view(url='settings/profile', permanent=False)),
    path('settings/profile', settings_profile, name='settings-profile'),
    path('settings/keys', settings_keys, name='settings-keys')
    # Repository
]

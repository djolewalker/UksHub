from django.urls import path
from django.views.generic import RedirectView
from .views import home, settings_keys, settings_profile

urlpatterns = [
    path('', home, name='home'),
    path('settings', RedirectView.as_view(url='settings/profile', permanent=False)),
    path('settings/profile', settings_profile, name='settings-profile'),
    path('settings/keys', settings_keys, name='settings-keys')
]

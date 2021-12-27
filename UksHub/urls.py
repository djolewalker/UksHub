from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = []

if settings.ADMIN_ENABLED is True:
    urlpatterns += [path('admin/', admin.site.urls)]

urlpatterns += [
    path('backoffice/', include('UksHub.apps.backoffice.urls')),
    path('', include('UksHub.apps.hub.urls'))
]

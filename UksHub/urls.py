from django.contrib import admin
from django.urls import path, include
from UksHub.apps.hubAuth.urls import urlpatterns as authUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backoffice/', include('UksHub.apps.backoffice.urls')),
    *authUrls,
    path('', include('UksHub.apps.hub.urls'))
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backoffice/', include('UksHub.apps.backoffice.urls')),
    path('', include('UksHub.apps.hub.urls'))
]

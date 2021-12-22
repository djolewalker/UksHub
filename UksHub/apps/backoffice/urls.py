from django.urls import path
from .views import backoffice

urlpatterns = [
    path('', backoffice, name='backoffice')
]
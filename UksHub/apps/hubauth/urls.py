from django.urls import path
from .views import createNewPassword, login, register, resetPassword

urlpatterns = [
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('reset-password', resetPassword, name='reset-passwort'),
    path('create-new-password', createNewPassword, name='create-new-password'),
]

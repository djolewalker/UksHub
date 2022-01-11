from django.urls import path
from .views import createNewPassword, login, logout, register, resetPassword

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', register, name='register'),
    path('reset-password', resetPassword, name='reset-passwort'),
    path('create-new-password', createNewPassword, name='create-new-password'),
]

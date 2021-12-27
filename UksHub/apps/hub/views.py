from django.http.response import HttpResponse
from django.shortcuts import render


def login(request):
    return render(request, 'hub/login.html')


def logout(request):
    return HttpResponse(status=204)


def register(request):
    return render(request, 'hub/register.html')


def resetPassword(request):
    return render(request, 'hub/reset-password.html')


def createNewPassword(request):
    return render(request, 'hub/create-new-password.html')


def home(request):
    return render(request, 'hub/home.html')

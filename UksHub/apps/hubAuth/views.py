from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SignupForm
from .services import createUser, loginUser, logoutUser


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if loginUser(
                    request, form.cleaned_data['username'], form.cleaned_data['password']):
                return redirect(request.GET.get('next', '/'))
            else:
                form.add_error(None, 'Invalid credentials!')
    else:
        form = LoginForm()
    return render(request, 'hub/login.html', {'form': form, 'next': request.GET.get('next') })


@login_required
def logout(request):
    if request.method == 'POST':
        logoutUser(request)
        return HttpResponse(status=204)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if createUser(request, form):
                return redirect('/')
            else:
                form.add_error(
                    None, 'Can\'t create user! Something went wrong.')
    else:
        form = SignupForm()
    return render(request, 'hub/register.html', {'form': form})


def resetPassword(request):
    return render(request, 'hub/reset-password.html')


def createNewPassword(request):
    return render(request, 'hub/create-new-password.html')
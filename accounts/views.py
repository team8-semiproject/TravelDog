# imports
from django.shortcuts import render, redirect

from .forms import (
    CustomAuthenticationForm as AuthenticationForm, 
    CustomPasswordChangeForm as PasswordChangeForm,
    CustomUserChangeForm as UserChangeForm,
    CustomUserCreationForm as UserCreationForm,
)
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth import get_user_model, update_session_auth_hash

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request, data=request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('places:index')
            # return redirect('places:places-list')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print("request", request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('places:index')
            # return redirect('places:places-list')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('places:index')
    # return redirect('places:places-list')


def profile(request, username):
    person = get_user_model().objects.get(username = username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.username)
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            auth_logout(request)
            return redirect('accounts:login')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password.html', context)


@login_required
def delete(request):
    request.user.delete()
    return redirect('accounts:login')
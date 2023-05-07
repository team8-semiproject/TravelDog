from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import (
    CustomAuthenticationForm as AuthenticationForm, 
    CustomPasswordChangeForm as PasswordChangeForm,
    CustomUserChangeForm as UserChangeForm,
    CustomUserCreationForm as UserCreationForm,
    
)


def signup(request):
    if request.method == "POST":
        print("request", request.POST)
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('places:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('places:index')
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


def profile(request, username):
    person = get_user_model().objects.get(username = username)
    context = {
        'person': person,
        'form':UserChangeForm(),
    }
    if person==request.user:
        context["form"] = UserChangeForm(instance=request.user)

    return render(request, 'accounts/profile.html', context)


@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        print(form.is_valid())
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


@login_required
def update_picture(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = UserChangeForm(instance=user, files=request.FILES)
        if form.is_valid():
            form.save()
    return redirect('accounts:profile', user.username)


@login_required
def delete_picture(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    user.picture.delete()
    return redirect('accounts:profile', user.username)

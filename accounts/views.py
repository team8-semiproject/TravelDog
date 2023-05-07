from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import redirect, render
from places.views import Place, Review
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
    person = get_user_model().objects.prefetch_related('bookmarked_places', 'user_reviews', 'like_reviews').get(username=username)
    my_reviews = Review.objects.filter(user=person).prefetch_related('place', 'place__photos', 'like')
    bookmark_places = Place.objects.prefetch_related('bookmark', 'photos', 'place_reviews').filter(bookmark=person)
    reviews_like = Review.objects.filter(like=person).prefetch_related('place', 'user', 'like', 'place__photos')
    raw_star = bookmark_places.annotate(avg_star=Avg('place_reviews__star'))
    stars = raw_star.values('id').annotate(avg_star=Avg('place_reviews__star'))

    if person==request.user:
        form = UserChangeForm(instance=request.user)
    else:
        form = UserChangeForm()

    context = {
        'person': person,
        'my_reviews': my_reviews,
        'bookmark_places' : bookmark_places,
        'like_reviews' : reviews_like,
        'stars': stars,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
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

# imports
from django.shortcuts import render, redirect
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from places.views import Place, Photo, Review
from django.core.paginator import Paginator
from django.conf import settings

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
        print("request", request.POST)
        form = UserCreationForm(data=request.POST)
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
    my_reviews = Review.objects.filter(user=person.pk)
    page = request.GET.get('page', '1')
    per_page = 8
    paginator = Paginator(my_reviews, per_page)
    page_object = paginator.get_page(page)
    my_photos = []
    for review in my_reviews:
        place = Place.objects.get(pk=review.place.pk)
        photo = place.photos.all()[:1]
        my_photos.append(photo)
    my_list = zip(my_reviews, my_photos)
    context = {
        'person': person,
        'reviews': page_object,
        'REST_API_KEY': settings.REST_API_KEY,
        'my_reviews': my_reviews,
        'my_list' : my_list
        
    }
    print(my_reviews,my_reviews.count)
    return render(request, 'accounts/profile.html', context)

    #     context = {
    #         'place': place,
    #         'reviews': page_object,
    #         'range': ['1', '2', '3', '4', '5'],
    #         'MAP_API_KEY': settings.MAP_API_KEY,
    #         'REST_API_KEY': settings.REST_API_KEY,
    #         'num_range': range(1,6),
    #     }
    #     return render(request, 'places/detail.html', context)

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
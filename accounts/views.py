from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
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
    
    // for 내가 쓴 리뷰
    my_reviews = Review.objects.filter(user=person.pk)
    page1 = request.GET.get('page', '1')
    per_page1 = 8
    paginator1 = Paginator(my_reviews, per_page1)
    page_object1 = paginator1.get_page(page1)
    
    // for 북마크
    bookmark_places = person.bookmarked_places.all()
    page2 = request.GET.get('page', '1')
    per_page2 = 12
    paginator2 = Paginator(bookmark_places, per_page2)
    page_object2 = paginator2.get_page(page2)
    
    // for 좋아요한 리뷰
    reviews_like = person.like_reviews.all()
    print('like_reviews',reviews_like)
    page3 = request.GET.get('page', '1')
    per_page3 = 8
    paginator3 = Paginator(reviews_like, per_page3)
    page_object3 = paginator3.get_page(page3)

    context = {
        'person': person,
        'my_reviews': page_object1,
        'bookmark_places' : page_object2,
        'like_reviews' : page_object3,
        'range1': ['1', '2', '3', '4', '5'],
        'range2': ['1', '2', '3', '4', '5'],
        'range3': ['1', '2', '3', '4', '5'],
    }
    
    // for update_profile modal
    if person==request.user:
        form = UserChangeForm(instance=request.user)
    else:
        form = UserChangeForm()
        
    context['form'] = form

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

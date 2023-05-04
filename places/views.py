import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PlaceForm, PhotoForm, ReviewForm
from .models import Place, Photo, Review


def index_redirect(request):
    return redirect('places:index')


def index(request):
    places = Place.objects.all()
    page = request.GET.get('page', '1')
    per_page = 16
    paginator = Paginator(places, per_page)
    page_object = paginator.get_page(page)
    context = {
        'places': page_object,
        'range': ['1', '2', '3', '4', '5'],
    }
    return render(request, 'places/index.html', context)


def create(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = PlaceForm(request.POST)
            photos = request.FILES.getlist('photo')
            if form.is_valid():
                place = form.save()
                if photos:
                    for photo in photos:
                        Photo.objects.create(place=place, photo=photo)
            return redirect('places:index')
        else:
            form = PlaceForm()
            photoform = PhotoForm()
        context = {
            'form': form,
            'photoform': photoform,
        }
        return render(request, 'places/create.html', context)
    return redirect('places:index')


def detail(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    reviews = Review.objects.filter(place=place)
    page = request.GET.get('page', '1')
    per_page = 8
    paginator = Paginator(reviews, per_page)
    page_object = paginator.get_page(page)
    review_form = ReviewForm()

    context = {
        'place': place,
        'reviews': page_object,
        'range': ['1', '2', '3', '4', '5'],
        'MAP_API_KEY': settings.MAP_API_KEY,
        'REST_API_KEY': settings.REST_API_KEY,
        'num_range': range(1,6),
    }
    return render(request, 'places/detail.html', context)


@login_required
def bookmark(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.bookmark.filter(pk=request.user.pk).exists():
        place.bookmark.remove(request.user)
        bookmarked = False
    else:
        place.bookmark.add(request.user)
        bookmarked = True
    context = {
        'bookmarked': bookmarked,
        'bookmark_count': place.bookmark.count(),
    }
    return JsonResponse(context)


def update(request, place_pk):
    if request.user.is_staff:
        PhotoFormSet = modelformset_factory(Photo, form=PhotoForm)
        place = get_object_or_404(Place, pk=place_pk)

        if request.method == 'POST':
            form = PlaceForm(request.POST, instance=place)
            formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.filter(place=place))

            if form.is_valid() and formset.is_valid():
                form.save()
                old_photos = Photo.objects.filter(place=place)
                for photoform in formset.cleaned_data:
                    if photoform:
                        photo = Photo(place=place, photo=photoform['photo'])
                        pre_save_photo(Photo, photo)
                        photo.save()
                return redirect('places:detail', place.pk)

        form = PlaceForm(instance=place)
        formset = PhotoFormSet(queryset=Photo.objects.filter(place=place))
        context = {
            'place': place,
            'form': form,
            'formset': formset,
        }
        return render(request, 'places/update.html', context)
    return redirect('places:detail', place.pk)


@receiver(pre_save, sender=Photo)
def pre_save_photo(sender, instance, *args, **kwargs):
    try:
        old_photo = instance.__class__.objects.get(pk=instance.pk).photo.path
        try:
            new_photo = instance.photo.path
        except:
            new_photo = None
        if new_photo != old_photo:
            import os
            if os.path.exists(old_photo):
                os.remove(old_photo)
    except:
        pass


def delete(request, place_pk):
    if request.user.is_staff:
        place = get_object_or_404(Place, pk=place_pk)
        photos = Photo.objects.filter(place=place)
        if photos:
            for photo in photos:
                post_save_photo(Photo, photo)
        place.delete()
        return redirect('places:index')
    return redirect('places:detail', place_pk)


@receiver(post_delete, sender=Photo)
def post_save_photo(sender, instance, *args, **kwargs):
    try:
        instance.photo.delete(save=False)
    except:
        pass


@login_required
def review_create(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    star = request.POST.get('star')
    content = request.POST.get('content')

    review = Review(star=star, content=content, place=place, user=request.user)
    review.save()
    return redirect('places:detail', place_pk)


@login_required
def review_like(request, place_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like.filter(pk=request.user.pk).exists():
        review.like.remove(request.user)
        is_liked = False
    else:
        review.like.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'likes_count': review.like.count()
    }
    return JsonResponse(context)


@login_required
def review_delete(request, place_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.user == request.user:
        review.delete()
    return redirect('places:detail', place_pk)


@login_required
def review_update(request, place_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            raw = list(request.POST.keys())
            data = json.loads(raw[0])
            review.content = data['content']
            # review.star = data['star']
            review.save()
    context = {
        'content': review.content,
        # 'star': review.star,
    }
    return JsonResponse(context)
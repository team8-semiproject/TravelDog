from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from .forms import PlaceForm, PhotoForm, ReviewForm
from .models import Place, Photo, Review
from django.core.paginator import Paginator

def index_redirect(request):
    return redirect('places:index')

def index(request):
    places = get_list_or_404(Place)
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
        PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=3)

        if request.method == 'POST':
            form = PlaceForm(request.POST)
            formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.none())

            if form.is_valid() and formset.is_valid():
                place = form.save()
                for photoform in formset.cleaned_data:
                    if photoform:
                        photo = Photo(place=place, photo=photoform['photo'])
                        photo.save()
                return redirect('places:index')
        else:
            form = PlaceForm()
            formset = PhotoFormSet(queryset=Photo.objects.none())
        context = {
            'form': form,
            'formset': formset,
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
        'num_range': range(1,6),
        'review_form': review_form,
    }
    return render(request, 'places/detail.html', context)


@login_required
def bookmark(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.bookmark.filter(pk=request.user.pk).exists():
        place.bookmark.remove(request.user)
    else:
        place.bookmark.add(request.user)
    return redirect('places:detail', place.pk)


def update(request, place_pk):
    if request.user.is_staff:
        PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=3)
        place = get_object_or_404(Place, pk=place_pk)

        if request.method == 'POST':
            form = PlaceForm(request.POST, request.FILES, instance=place)
            formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.filter(place=place))

            if form.is_valid() and formset.is_valid():
                form.save()
                for photoform in formset.cleaned_data:
                    if photoform:
                        photo = Photo(place=form, photo=photoform['photo'])
                        photo.save()
                return redirect('places:detail', place.pk)
        else:
            form = PlaceForm(instance=place)
            formset = PhotoFormSet(queryset=Photo.objects.filter(place=place))
        context = {
            'form': form,
            'formset': formset,
            'place': place,
        }
        return render(request, 'places/update.html', context)
    return redirect('places:detail', place_pk)


def delete(request, place_pk):
    if request.user.is_staff:
        place = get_object_or_404(Place, pk=place_pk)
        place.delete()
        return redirect('places:index')
    return redirect('places:detail', place_pk)


@login_required
def review_create(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # form = ReviewForm(request.POST)
    # if form.is_valid():
    #     review = form.save(commit = False)
    #     review.place = place
    #     review.user = request.user
    #     review.save()
    #     return redirect('places:detail', place_pk)
    star = request.POST.get('star')
    content = request.POST.get('content')

    review = Review(star=star, content=content, place=place, user=request.user)
    review.save()
    return redirect('places:detail', place_pk)

    context = {
        'place': place,
        # 'form': form,
    }
    return render(request, 'places/review.html', context)

@login_required
def review_like(request, place_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like.filter(pk=request.user.pk).exists():
        review.like.remove(request.user)
    else:
        review.like.add(request.user)
    return redirect('places:detail', place_pk)


@login_required
def review_delete(request, place_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.user == request.user:
        review.delete()
    return redirect('places:detail', place_pk)

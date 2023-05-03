from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from .forms import PlaceForm, PhotoForm, ReviewForm
from .models import Place, Photo, Review


class PlaceListView(View):
    def get(self, request):
        places = get_list_or_404(Place)
        context = {
            'places': places,
        }
        return render(request, 'places/index.html', context)


class PlaceDetailView(View):
    def get(self, request, place_pk):
        place = get_object_or_404(Place, pk=place_pk)
        context = {
            'place': place,
        }
        return render(request, 'places/detail.html', context)


    def delete(self, request, place_pk):
        if request.user.is_superuser or request.user.is_staff:
            place = get_object_or_404(Place, pk=place_pk)
            place.delete()
            return redirect('places:index')
        return redirect('places:detail', place_pk)


class Review(View):
    @method_decorator(login_required)
    def post(self, request, place_pk):
        place = get_object_or_404(Place, pk=place_pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit = False)
            review.place = place
            review.user = request.user
            review.save()
            return redirect('places:detail', place_pk)
        context = {
            'review': review,
            'form': form,
        }
        return render(request, 'places/detail.html', context)
    

    def delete(self, request, place_pk, review_pk):
        review = get_object_or_404(Review, pk=review_pk)
        if review.user == request.user:
            review.delete()
        return redirect('places:detail', place_pk)


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


def update(request, place_pk):
    if request.user.is_staff:
        PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=3)
        place = get_object_or_404(Place, pk=place_pk)

        if request.method == 'POST':
            form = PlaceForm(request.POST, instance=request.data)
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
        }
        return render(request, 'places/update.html', context)
    return redirect('places:detail', place_pk)
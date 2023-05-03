from django import forms
from .models import Place, Photo, Review


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'address', 'latitude', 'longtitude',)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('photo',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content', 'star',)
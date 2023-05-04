from django import forms
from .models import Place, Photo, Review

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'address',)


class PhotoForm(forms.ModelForm):
    photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Photo
        fields = ('photo',)


class ReviewForm(forms.ModelForm):
    star = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5, 'id': 'starRange'}))

    class Meta:
        model = Review
        fields = ('star', 'content',)
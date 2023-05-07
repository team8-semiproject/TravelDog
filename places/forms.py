from django import forms
from .models import Place, Photo, Review


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'address',)


class PhotoForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}))
    class Meta:
        model = Photo
        fields = ('photo',)


class PhotoUpdateForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.ClearableFileInput)
    class Meta:
        model = Photo
        fields = ('photo',)
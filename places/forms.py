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
  
    star = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5, 'id': 'starRange'}))

    class Meta:
        model = Review
        fields = ('star', 'content',)
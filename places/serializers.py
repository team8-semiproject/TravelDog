from rest_framework import serializers
from .models import Place, Photo, Review


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo',)


class PlaceSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = ('pk', 'name', 'address', 'latitude', 'longtitude', 'photos',)

    def create(self, validated_data):
        photos_data = self.context['request'].FILES
        place = Place.objects.create(**validated_data)
        for photo_data in photos_data.getlist('photo'):
            Photo.objects.create(place=place, photo=photo_data)
        return place


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Review
        fields = '__all__'
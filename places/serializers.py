from rest_framework import serializers
from .models import Place, Photo, Review


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo',)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('Place',)


class PlaceSerializer(serializers.ModelSerializer):
    class PlaceReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = '__all__'

    photos = PhotoSerializer(many=True, read_only=True)
    reviews = PlaceReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)

    class Meta:
        model = Place
        fields = '__all__'

    def create(self, validated_data):
        photos_data = self.context['request'].FILES
        place = Place.objects.create(**validated_data)
        for photo_data in photos_data.getlist('photo'):
            Photo.objects.create(place=place, photo=photo_data)
        return place
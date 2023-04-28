from rest_framework import serializers
from .models import Place, Photo, Review


class PhotoSerializer(serializers.ModelSerializer):
    photos = serializers.ImageField(use_url=True)
    class Meta:
        model = Photo
        fields = ('photos',)


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class PlaceReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = '__all__'

    review_set = PlaceReviewSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)

    def get_photos(self, object):
        photo = object.photos.all()
        return PhotoSerializer(instance=photo, many=True, context=self.context).data

    class Meta:
        model = Place
        fields = ('name', 'address', 'photos',)
    
    def create(self, validated_data):
        instance = Place.objects.create(**validated_data)
        photo_set = self.context['request'].FILES
        for photo_data in photo_set.getlist('photos'):
            Photo.objects.create(diary=instance, photo=photo_data)
        return instance


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
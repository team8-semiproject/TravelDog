from rest_framework import serializers
from .models import Place, Photo, Review


class PhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True)
    class Meta:
        model = Photo
        fields = ('photo',)


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class PlaceReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = '__all__'

    review_set = PlaceReviewSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)

    def get_photo(self, object):
        photo = object.photos.all()
        return PhotoSerializer(instance=photo, many=True, context=self.context).data

    class Meta:
        model = Place
        fields = ('name', 'address', 'photo', 'review_set', 'review_count',)
    
    def create(self, validated_data):
        instance = Place.objects.create(**validated_data)
        photo_set = self.context['request'].FILES
        for photo_data in photo_set.getlist('photo'):
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
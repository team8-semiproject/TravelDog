from django.db import models
from django.conf import settings
from accounts.models import User


class Place(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longtitude = models.FloatField()
    bookmark = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_places', blank=True)

    def __str__(self):
        return str(self.name)


class Photo(models.Model):
    def photo_path(instance, filename):
        return f'places/{instance.place.pk}/{filename}'

    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=photo_path)

    def __str__(self):
        return str(self.place)


class Review(models.Model):
    point = zip(range(1, 6), range(1, 6))

    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews')
    content = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews', blank=True)
    star = models.IntegerField(choices=point)

    def __str__(self):
        return str(self.place) + ' - ' + str(self.user)
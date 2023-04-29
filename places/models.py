from django.db import models
from accounts.models import User


class Place(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longtitude = models.FloatField()
    bookmark = models.ManyToManyField(User, related_name='bookmarked_places')

    def __str__(self):
        return str(self.name)


class Photo(models.Model):
    def photo_path(instance, filename):
        return f'{instance.place.name}/{filename}'

    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=photo_path)

    def __str__(self):
        return str(self.place)


class Review(models.Model):
    point = zip(range(1, 6), range(1, 6))

    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300, blank=True, null=True)
    like = models.ManyToManyField(User, related_name='like_reviews')
    star = models.IntegerField(choices=point)

    def __str__(self):
        return str(self.place) + ' - ' + str(self.user)
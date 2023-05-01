from .models import Place, Review
from .serializers import PlaceSerializer, ReviewSerializer
from rest_framework.viewsets import ModelViewSet


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
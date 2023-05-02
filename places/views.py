from rest_framework.viewsets import ModelViewSet
from .models import Place, Review
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import PlaceSerializer, ReviewSerializer


class PlaceViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class ReviewViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Place, Review
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import PlaceSerializer, ReviewSerializer


class PlaceViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]


    def list(self, request):
        places = Place.objects.all()
        return Response({'places': places}, template_name='places/index.html')


    def retrieve(self, request, pk):
        place = Place.objects.get(pk=pk)
        return Response({'place': place}, template_name='places/detail.html')


    def create(self, request):
        serializer = PlaceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        place = serializer.save()
        return redirect('places:detail', place.pk)


    def update(self, request, pk):
        place = Place.objects.get(pk=pk)
        serializer = PlaceSerializer(place, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'place': place})
        serializer.save()
        return redirect('places:detail', pk)


    def destroy(self, request, pk):
        place = Place.objects.get(pk=pk)
        place.delete()
        return redirect('places:index')


class ReviewViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]


    def list(self, request, pk):
        place = Place.objects.get(pk=pk)
        review = Review.objects.get(place=place)
        return Response({'review': review }, template_name='places/detail.html')


    def create(self, request):
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('places:index')


    def update(self, request, pk):
        review = Review.objects.get(pk=pk)
        place = review.place
        serializer = ReviewSerializer(review, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'review': review})
        serializer.save()
        return redirect('places:detail', place.pk)


    def destroy(self, request, pk):
        review = Review.objects.get(pk=pk)
        place = review.place
        review.delete()
        return redirect('places:detail', place.pk)


    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
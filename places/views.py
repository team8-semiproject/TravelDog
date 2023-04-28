from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PlaceListSerializer, PlaceSerializer, ReviewListSerializer, ReviewSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Place, Photo, Review


@api_view(['GET', 'POST'])
def place_list(request):
    if request.method == 'GET':
        places = get_list_or_404(Place)
        serializer = PlaceListSerializer(places, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        if request.user.is_superuser:
            serializer = PlaceSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'DELETE', 'PUT'])
def place_detail(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if request.method == 'GET':
        serializer = PlaceSerializer(place)
        return Response(data=serializer.data)
    elif request.user.is_superuser:
        if request.method == 'DELETE':
            place.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            serializer = PlaceSerializer(place, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def review_list(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if request.method == 'GET':
        reviews = get_list_or_404(Review, place=place)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(data=serializer.data)
    elif request.user.is_authenticated:
        if request.method == 'POST':
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(place=place)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return login_required()


@api_view(['GET', 'DELETE', 'PUT'])
def review_detail(request, place_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(data=serializer.data)
    if request.use == review.user:
        if request.method == 'DELETE':
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
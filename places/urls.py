from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('', views.PlaceViewSet, basename='places')
router.register('reviews', views.ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
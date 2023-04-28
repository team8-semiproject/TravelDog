from django.urls import path
from . import views


app_name = 'places'
urlpatterns = [
    path('', views.place_list),
    path('<int:place_pk>/', views.place_detail),
    path('<int:place_pk>/reviews/', views.review_list),
    path('<int:place_pk>/reviews/<review_pk>/', views.review_detail),
]
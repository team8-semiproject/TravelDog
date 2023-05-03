from django.urls import path
from . import views


app_name = 'places'
urlpatterns = [
    path('', views.PlaceListView.as_view(), name='index'),
    path('create/', views.create, name='create'),
    path('update/<int:place_pk>/', views.update, name='update'),
    path('<int:place_pk>/', views.PlaceDetailView.as_view(), name='detail'),
    path('<int:place_pk>/review/', views.Review.as_view(), name='review'),
    path('<int:place_pk>/review/delete/<int:review_pk>/', views.Review.as_view(), name='review_delete'),
    path('<int:place_pk>/review/update/<int:review_pk>/', views.Review.as_view())
]

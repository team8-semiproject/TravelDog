from django.urls import path
from . import views


app_name = 'places'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:place_pk>/', views.detail, name='detail'),
    path('<int:place_pk>/bookmark/', views.bookmark, name='bookmark'),
    path('update/<int:place_pk>/', views.update, name='update'),
    path('delete/<int:place_pk>/', views.delete, name='delete'),
    path('<int:place_pk>/review/', views.review_create, name='review_create'),
    path('<int:place_pk>/review/like/<int:review_pk>/', views.review_like, name='review_like'),
    path('<int:place_pk>/review/delete/<int:review_pk>/', views.review_delete, name='review_delete'),
    path('<int:place_pk>/review/update/<int:review_pk>/', views.review_update, name='review_update'),
]
from django.urls import path
from . import views


app_name = 'places'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:place_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('update/<int:place_pk>/', views.update, name='update'),
    path('delete/<int:place_pk>/', views.delete, name='delete'),
    path('<int:place_pk>/review/', views.review_create, name='review_create'),
    path('<int:place_pk>/review/delete/<int:review_pk>/', views.review_delete, name='review_delete'),
]
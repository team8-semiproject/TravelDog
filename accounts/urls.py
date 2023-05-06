from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('update_picture/', views.update_picture, name="update_picture"),
    path('delete_picture/', views.delete_picture, name="delete_picture"),
    path('password/', views.password, name="password"),
    path('delete/', views.delete, name="delete"),
]
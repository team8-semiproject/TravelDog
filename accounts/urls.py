from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'accounts'
urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.signup, name="logout"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('update/', views.update, name="update"),
    path('password/', views.password, name="password"),
    path('delete/', views.delete, name="delete"),
]
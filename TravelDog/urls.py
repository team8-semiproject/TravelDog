from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from places import views


urlpatterns = [
    path('', views.index_redirect),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('places/', include('places.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

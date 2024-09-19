from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.catalog, name='catalog_with_slug'),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

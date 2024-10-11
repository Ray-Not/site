from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from  web.sitemaps import BlogSitemap, DoorSitemap

handler404 = 'web.views.custom_404_view'

sitemaps = {
    'blogs': BlogSitemap,
    'doors': DoorSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

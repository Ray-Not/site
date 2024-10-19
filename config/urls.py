from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from web.sitemaps import (BlogSitemap, ContactPageSitemap, DeliveryPageSitemap,
                          DoorSitemap, HomePageSitemap)

handler404 = 'web.views.custom_404_view'

sitemaps = {
    'blogs': BlogSitemap,
    'doors': DoorSitemap,
    'index': HomePageSitemap,
    'contact': ContactPageSitemap,
    'delivery': DeliveryPageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('captcha/', include('captcha.urls')),
    path('', include('web.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

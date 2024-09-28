from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from django.conf.urls import handler404


handler404 = 'web.views.custom_404_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

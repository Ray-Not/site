from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('contacts/', views.contact, name='contact'),
    path('compare/', views.compare_doors, name='compare_doors'),
    path('delivery/', views.delivery, name='delivery'),
    path(
        'delivery/<slug:slug>/',
        views.delivery_detail,
        name='delivery_detail'
    ),
    path('installation/', views.installation, name='installation'),
    path('garant/', views.garant, name='garant'),
    path('calc/', views.calculator, name='calculator'),
    path('shop_card/', views.shop_card, name='shop_card'),
    path('reviews/', views.reviews, name='reviews'),
    path('detail/<slug:slug>/', views.door_detail, name='door_detail'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.catalog, name='catalog_with_slug'),
    path('blog/', views.blog_chapter, name='blog_chapter'),
    path(
        'blog/<slug:chapter_slug>/',
        views.blog_chapter_detail,
        name='blog_chapter_detail'
    ),
    path(
        'blog/<slug:chapter_slug>/<slug:post_slug>/',
        views.blog_post_detail,
        name='blog_post_detail'
    ),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Blog, Door, Catalog


class CatalogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Catalog.objects.all()


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class DoorSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Door.objects.filter(hidden=False)

    def lastmod(self, obj):
        return obj.created_at


class HomePageSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)


class DeliveryPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['delivery']

    def location(self, item):
        return reverse(item)


class ContactPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['contact']

    def location(self, item):
        return reverse(item)

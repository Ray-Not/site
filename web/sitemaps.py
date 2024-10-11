from django.contrib.sitemaps import Sitemap
from .models import Blog, Door


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
        return Door.objects.all()

    def lastmod(self, obj):
        return obj.created_at

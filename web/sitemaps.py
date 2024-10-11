from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import YourModel  # Импортируйте свои модели

class YourModelSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return YourModel.objects.all()  # Возвращает все объекты вашей модели

    def location(self, item):
        return reverse('yourmodel_detail', args=[item.pk])  # Укажите ваш URL

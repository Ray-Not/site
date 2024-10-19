from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (Blog, BlogChapter, CallBack, Catalog, CustomOrder,
                     DeliveryRegion, Door, GetDiscount, Order, Review, Tag)


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'price', 'purpose', 'created_at')
    ordering = ('id',)


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(DeliveryRegion)
class DeliveryRegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone', 'order_number', 'view_door_link', 'message'
    )

    def view_door_link(self, obj):
        if obj.door:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('door_detail', args=[obj.door.slug]),
                obj.door.title
            )
        return "Нет двери"

    view_door_link.short_description = 'Дверь'


admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(BlogChapter)
admin.site.register(CustomOrder)
admin.site.register(GetDiscount)
admin.site.register(CallBack)

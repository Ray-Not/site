from django.contrib import admin

from .models import Door, Order, Tag, Catalog, Review, Blog, BlogChapter, DeliveryRegion, Equipment


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'purpose')
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


admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(BlogChapter)
admin.site.register(Equipment)

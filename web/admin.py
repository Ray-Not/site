from django.contrib import admin

from .models import Door, Order, Tag, Catalog


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'purpose')
    ordering = ('id',)


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Order)
admin.site.register(Tag)

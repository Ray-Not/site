from django.contrib import admin

from .models import Door, Order, Review, Tag

admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Tag)


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title', 'purpose')
    list_filter = ('id', 'purpose', 'steel_size')

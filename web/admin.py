from django.contrib import admin

from .models import Door, Order, Tag


class DoorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'purpose')
    ordering = ('id',)


admin.site.register(Door, DoorAdmin)
admin.site.register(Order)
admin.site.register(Tag)

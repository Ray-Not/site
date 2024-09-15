from django.contrib import admin

from .models import Door, Order


class DoorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'purpose')
    ordering = ('id',)


admin.site.register(Door, DoorAdmin)
admin.site.register(Order)

from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields = [
        'id',
    ]

    list_display = [
        'title',
        'starts_at',
        'ends_at',
        'id',
    ]

    ordering = ['starts_at']

from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields = [
        'get_image_preview',
        'id',
    ]

    list_display = [
        'title',
        'starts_at',
        'ends_at',
        'get_image_list_preview',
        'rating',
        'id',
    ]

    ordering = ['starts_at']

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html(
            '<img src="{url}" style="max-height: 200px;"/>',
            url=obj.image.url
        )

    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:timetable_event_change', args=(obj.id,))
        return format_html(
            '<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/>\
                </a>',
            edit_url=edit_url, src=obj.image.url
        )
    get_image_list_preview.short_description = 'превью'

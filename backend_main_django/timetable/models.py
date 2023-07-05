from django.db import models
from django.utils.timezone import localtime


class Event(models.Model):
    title = models.CharField(
        verbose_name='заголовок',
        max_length=100,
    )
    starts_at = models.DateTimeField(
        verbose_name='начинается в '
    )
    ends_at = models.DateTimeField(
        verbose_name='завершается в ',
        blank=True,
        null=True,
    )

    class Meta():
        verbose_name = 'событие'
        verbose_name_plural = 'события'

    def __str__(self):
        return (
            f'{self.title} '
            f'({localtime(self.starts_at).strftime("%d.%m.%Y %H:%M")})'
        )

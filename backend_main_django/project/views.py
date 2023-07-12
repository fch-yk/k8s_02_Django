from django.shortcuts import render
from timetable.models import Event


def index(request):
    context = {
        'title': 'Experimental k8s website',
        'version': 'version 12.07.2023 18:59',
        'events': Event.objects.all().order_by('starts_at'),
    }
    return render(request, 'index.html', context=context)

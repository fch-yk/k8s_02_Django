from django.shortcuts import render
from timetable.models import Event


def index(request):
    context = {
        'title': 'Experimental k8s website',
        'version': 'version 08.07.2023 17:01',
        'events': Event.objects.all().order_by('starts_at'),
    }
    return render(request, 'index.html', context=context)

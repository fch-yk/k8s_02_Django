from django.shortcuts import render


def index(request):
    context = {
        'title': 'Experimental k8s website',
        'version': 'version 07.07.2023 22:41',
    }
    return render(request, 'index.html', context=context)

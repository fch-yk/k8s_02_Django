from django.http import HttpResponse


def index(request):
    return HttpResponse('Test k8s website, version 03.07.2023 14:42')

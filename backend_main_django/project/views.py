from django.http import HttpResponse


def index(request):
    return HttpResponse('Test k8s website, version 05.07.2023 10:38')

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from . import models


# Create your views here.


def home(request):
    return render(request, 'index.html', {})


def pc(request, id=None):
    instance = get_object_or_404(models.Pc, id=id)
    return HttpResponse(instance.getSpecs())

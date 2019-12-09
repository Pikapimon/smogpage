from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
# Create your views here.
import json


def homepage(request):
    return render(request, 'prediction/index.html', {})


def history_refresh(request):
    a = {1: 2}
    return JsonResponse(a)

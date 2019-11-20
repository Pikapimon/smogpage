from django.shortcuts import render
from django.views import generic
# Create your views here.


def homepage(request):
    return render(request, 'prediction/index.html', {})

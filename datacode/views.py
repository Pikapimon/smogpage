from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'datacode/total.html')


def frame1(request):
    return render(request, 'datacode/first.html')

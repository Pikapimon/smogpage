from django.http import HttpResponse
from django.shortcuts import render
import datetime

# def hello(request):
#     return HttpResponse("Hello Django!!")


def hello(request):
    context = {}
    context["hello"] = "Hello Django Template!!"
    context["athletes"] = ["Ming", "Zhi", "Dog"]
    context["now_date"] = datetime.date.today()
    return render(request, "hello.html", context)


def smog(request):
    context = {}
    context["hello"] = "Hello Django Template!!"
    return render(request, "index.html")

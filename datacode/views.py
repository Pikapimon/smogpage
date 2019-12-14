from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
import json
import os
from .models import Data


def total(request):
    return render(request, 'datacode/total.html')


def first(request):
    return render(request, 'datacode/first.html')


def second(request):
    return render(request, 'datacode/second.html')


def three(request):
    return render(request, 'datacode/three.html')


# 第一个页面
def sendfirstdata(request):
    if request.method == 'GET':
        # 处理函数

        # 返回结果
        return HttpResponse(json.dumps({
            'imgpath':  '',
            'name': 'hurui'
        }))

    if request.method == 'POST':
        files = request.FILES.get('file')
        # 保存上传的文件
        data = Data(name=files.name, files=files)
        data.save()

        # 处理

        return HttpResponse(json.dumps({
            'imgpath': '/'
        }))
    return render(request, 'datacode/total.html')


def sendsecdata(requset):
    if requset.method == 'POST':
        function = requset.POST.get('function')  # 方法
        Kvalue = requset.POST.get('Kvalue')    # k值
        files = requset.FILES.get('file')  # 数据
        data = Data(name=files.name, files=files)
        data.save()

        # 处理
        print(function, Kvalue)

        return HttpResponse(json.dumps({
            'imgpath': ''
        }))
    return render(requset, 'datacode/total.html')


def sendthirddata(request):
    if request.method == 'POST':
        files = request.FILES.get('file')
        # 保存上传的文件
        data = Data(name=files.name, files=files)
        data.save()

        # 处理

        return HttpResponse(json.dumps({
            'result': '我收到了'
        }))
    return render(request, 'datacode/total.html')

# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
import json
import os
from .models import Data
from .process.console import *
from django.conf import settings


def total(request):
    return render(request, 'datacode/total.html')


def first(request):
    return render(request, 'datacode/first.html')


def second(request):
    return render(request, 'datacode/second.html')


def three(request):
    return render(request, 'datacode/three.html')


def four(request):
    return render(request, 'datacode/four.html')


def five(request):
    return render(request, 'datacode/five.html')

# 第一个页面


def sendfirstdata(request):
    if request.method == 'GET':
        # 处理函数
        a = request.dict()

        return HttpResponse(json.dumps(a))
        # 返回结果
        return HttpResponse(json.dumps({
            'imgpath':  'sd',
            'name': 'hurui'
        }))

    if request.method == 'POST':
        files = request.FILES.get('file')
        # 保存上传的文件
        data = Data(name=files.name, files=files)
        data.save()
        sup = float(request.POST['sup'])
        con = float(request.POST['con'])
        # 处理
        pro = process(os.path.join(
            settings.BASE_DIR, 'data.xlsx'), 1, [sup, con])
        a, b = (pro.start())
        # a返回的结果为频繁项集
        print(b)
        result = []
        for keys in b:
            tmp = []
            tmp.append(list(list(keys)[0]))
            tmp.append(list(list(keys)[1]))
            print(b[keys].keys())
            tmp.append(b[keys]['confidence：'])
            tmp.append(b[keys]['support:'])
            tmp.append(b[keys]['lift:'])
            print(keys, b[keys])
            result.append(tmp)
        a = [a, result]
        return HttpResponse(json.dumps(a), content_type="application/json,charset=utf8")
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

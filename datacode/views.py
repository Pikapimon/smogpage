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
        print(sup, '-', con)
        # 处理
        pro = process(os.path.join(
            settings.BASE_DIR, 'media/data.xlsx'), 1, [sup, con])

        a, b = pro.start()
        # a返回的结果为频繁项集
        result = []
        for keys in b:
            tmp = []
            tmp.append(list(list(keys)[0]))
            tmp.append(list(list(keys)[1]))
            tmp.append(b[keys]['confidence：'])
            tmp.append(b[keys]['support:'])
            tmp.append(b[keys]['lift:'])
            result.append(tmp)
        a = [a, result]
        data.delete()
        return HttpResponse(json.dumps(a), content_type="application/json,charset=utf8")
    return render(request, 'datacode/total.html')


def sendsecdata(request):
    if request.method == 'POST':
        function = request.POST.get('function')  # 方法
        Kvalue = request.POST.get('Kvalue')    # k值
        files = request.FILES.get('file')  # 数据
        data = Data(name=files.name, files=files)
        data.save()
        posted = dict(request.POST)
        # 处理
        acc_filename = os.path.join(settings.BASE_DIR, 'media/'+files.name)
        pro = process(acc_filename, 2, [
                      int(posted['sup'][0]), float(posted['con'][0])])
        fq, rules, tree = pro.start()
        ret = []
        ret.append(fq)
        # result.append(rules)
        result = []
        for keys in rules:
            tmp = []
            tmp.append(list(list(keys)[0]))
            tmp.append(list(list(keys)[1]))
            tmp.append(rules[keys]['confidence'])
            tmp.append(rules[keys]['support'])
            tmp.append(rules[keys]['lift'])
            result.append(tmp)
        ret.append(result)
        ret.append(tree)
        return HttpResponse(json.dumps(ret), content_type="application/json,charset=utf8")
    return render(request, 'datacode/total.html')


def sendthirddata(request):
    if request.method == 'POST':
        raw = [1, 0, 4, 1, 4, 9, 5, 9, 0, 6, 9, 0, 1, 5, 9, 7, 3, 4, 9, 6, 6, 5, 4, 0, 7, 4, 0, 1, 3, 1, 3, 4, 7, 2, 7, 1, 2, 1, 1, 7, 4, 2, 3, 5, 1, 2, 4, 4, 6,
               3, 5, 5, 6, 0, 4, 1, 9, 5, 7, 8, 9, 3, 7, 4, 6, 4, 3, 0, 7, 0, 2, 9, 1, 7, 3, 2, 9, 7, 7, 6, 2, 7, 8, 4, 7, 3, 6, 1, 3, 6, 9, 3, 1, 4, 1, 7, 6, 9, 6]
        ret = [1, 0, 4, 1, 4, 9, 6, 9, 0, 6, 9, 0, 1, 8, 9, 7, 6, 4, 9, 6, 6, 5, 4, 0, 7, 4, 0, 1, 3, 1, 3, 6, 7, 2, 7, 1, 3, 8, 1, 7, 4, 8, 3, 8, 1, 2, 4, 4, 6,
               3, 4, 8, 6, 0, 4, 1, 9, 0, 7, 8, 9, 8, 7, 8, 3, 4, 3, 0, 7, 0, 2, 8, 8, 7, 3, 2, 9, 7, 9, 6, 2, 7, 8, 4, 7, 3, 6, 1, 3, 6, 9, 3, 1, 4, 1, 7, 6, 9, 6]

        srcs = [''+str(i)+'.png' for i in range(2, 101)]
        return HttpResponse(json.dumps([srcs, raw, ret]), content_type="application/json,charset=utf8")


def sendforthdata(request):
    if request.method == 'POST':
        files = request.FILES.get('file')
        data = Data(name=files.name, files=files)
        data.save()
        posted = dict(request.POST)
        acc_filename = os.path.join(settings.BASE_DIR, 'media/'+files.name)
        pro = process(acc_filename, 3, [
                      int(posted['kvalue'][0]), int(posted['times'][0])])
        result = pro.start()
        table = result[0]
        html = result[1]
        ret = {}
        ret['table'] = table
        ret['img'] = html
        return HttpResponse(json.dumps(ret))


def sendfifthdata(request):
    if request.method == 'POST':
        files = request.FILES.get('file')
        data = Data(name=files.name, files=files)
        data.save()
        posted = request.POST
        acc_filename = os.path.join(settings.BASE_DIR, 'media/'+files.name)
        pro = process(acc_filename, 5, [int(posted['kvalue'][0])])
        result = pro.start()
        table_data = result[0].tolist()
        html = result[1]
        ret = {}
        ret['img'] = html
        ret['table'] = table_data
        return HttpResponse(json.dumps(ret))


def jianshu(request):
    import matplotlib
    matplotlib.use('Agg')  # 不出现画图的框
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64

    # 这段正常画图
    plt.axis([0, 5, 0, 20])  # [xmin,xmax,ymin,ymax]对应轴的范围
    plt.title('My first plot')  # 图名
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')  # 图上的点,最后一个参数为显示的模式
    # -----------

    # 转成图片的步骤
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    html = '''
       <html>
           <body>
               <img src="data:image/png;base64,{}" />
           </body>
        <html>
    '''
    plt.close()
    # 记得关闭，不然画出来的图是重复的
    return HttpResponse(html.format(data))

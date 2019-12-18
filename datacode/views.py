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
        print(rules)
        return HttpResponse(json.dumps(ret), content_type="application/json,charset=utf8")
    return render(request, 'datacode/total.html')


def sendthirddata(request):
    if request.method == 'POST':
        from io import BytesIO
        import base64
        files = request.FILES.get('file')
        # 保存上传的文件
        data = Data(name=files.name, files=files)
        data.save()
        posted = dict(request.POST)
        # 处理
        acc_filename = os.path.join(settings.BASE_DIR, 'media/'+files.name)
        pro = process(acc_filename, 4, [
                      int(posted['punish'][0]), posted['method'][0], 1])
        result = pro.start()
        ret = {}
        for i in range(1, 4):
            ret[str(i)] = result[i]
        return HttpResponse(json.dumps(ret), content_type="application/json,charset=utf8")


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
        print(result)
        table = result[0]
        plt = result[1]
        from io import BytesIO
        import base64
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()
        html = 'data:image/png;base64,{} '
        ret = {}
        ret['table'] = table
        ret['img'] = html.format(data)
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
        plt = result[1]
        from io import BytesIO
        import base64
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()
        html = 'data:image/png;base64,{} '
        ret = {}
        ret['img'] = html.format(data)
        ret['table'] = table_data
        print(type(table_data))
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
    print(data)
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

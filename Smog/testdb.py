from django.http import HttpResponse

from TestModel.models import day_data

# 数据库操作


def testdb(request):
    response = ""
    list1 = day_data.objects.all()
    for var in list1:
        response += var.name+" "
        return HttpResponse("<p>"+response+"</p>")

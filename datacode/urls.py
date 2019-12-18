from django.urls import path
from . import views

app_name = 'datacode'
urlpatterns = [
    path('', views.total, name="datacode_homepage"),
    path('first/', views.first, name='first_frame'),
    path('second/', views.second, name='second_frame'),
    path('third/', views.three, name='third_frame'),
    path('forth/', views.four, name='forth_frame'),
    path('fifth/', views.five, name='fifth_frame'),

    path('sendfirstdata/', views.sendfirstdata, name='upload1'),
    path('sendsecdata/', views.sendsecdata, name='upload2'),
    path('sendhirddata/', views.sendthirddata, name='upload3'),
    path('sendforthdata/', views.sendforthdata, name='upload4'),
    path('sendfifthdata/', views.sendfifthdata, name='upload5'),
    path('jianshu/', views.jianshu, name='getimg')

]

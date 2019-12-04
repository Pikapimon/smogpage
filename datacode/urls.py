from django.urls import path
from . import views

app_name = 'datacode'
urlpatterns = [
    path('', views.index, name="datacode_homepage"),
    path('first', views.frame1, name='first_frame'),

]

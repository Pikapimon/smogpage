from django.urls import path
from . import views

app_name = 'prediction'
urlpatterns = [
    path('', views.homepage, name="home"),
    path('ajax-province-refresh/', views.history_refresh,
         name="history-province-refresh"),

]

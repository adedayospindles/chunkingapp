from django.urls import path 
from .views import homePage, splitCSV, csvToJson, save, delete, jsonToCsv

urlpatterns = [
    path('', homePage, name="home"),
    path('csvsplit/', splitCSV, name="splitcsv"),
    path('csv2json/', csvToJson, name="csv2json"),
    path('json2csv/', jsonToCsv, name="json2csv"),
    path('save/<str:pk>/', save, name="save"),
    path('delete/<str:pk>/', delete, name="delete"),
]


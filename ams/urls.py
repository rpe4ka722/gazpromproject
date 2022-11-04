from django.urls import path
from . import views

app_name = 'ams'
urlpatterns = [
    path('', views.ams, name='ams')
    ]

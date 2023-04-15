from django.urls import path
from . import views

app_name = 'ams'
urlpatterns = [
    path('', views.ams, name='ams'),
    path('ams_create/', views.ams_create, name='ams_create'),
    path('export_xls_ams/', views.export_xls_ams, name='export_xls_ams'),
    path('delete_ams/<int:ams_id>/', views.delete_ams, name='delete_ams'),
    path('ams_detail/<int:ams_id>/', views.ams_detail, name='ams_detail'),
    ]

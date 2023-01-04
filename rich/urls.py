from django.urls import path
from . import views

app_name = 'rich'
urlpatterns = [
    path('', views.rich_index, name='rich_index')
]

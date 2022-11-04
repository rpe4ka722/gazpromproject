from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.user_profile, name='user_status'),
    path('login', views.user_login, name='login'),
    path('registration', views.create_user, name='registration'),
    path('profile', views.user_profile, name='user_profile'),
    path('logout', views.logout_view, name='logout'),
    path('change_first_name', views.change_first_name, name='change_first_name'),
    path('change_last_name', views.change_last_name, name='change_last_name'),
    path('change_email', views.change_email, name='change_email'),
    path('change_department', views.change_department, name='change_department'),
    path('change_password', views.change_password, name='change_password')
]

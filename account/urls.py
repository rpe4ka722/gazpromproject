from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.user_profile, name='user_status'),
    path('login', views.user_login, name='login'),
    path('user_detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('logout', views.logout_view, name='logout'),
    path('change_first_name/<int:user_id>/', views.change_first_name, name='change_first_name'),
    path('change_last_name/<int:user_id>/', views.change_last_name, name='change_last_name'),
    path('change_email/<int:user_id>/', views.change_email, name='change_email'),
    path('password_reset/<int:user_id>', views.password_reset, name='password_reset'),
    path('change_department/<int:user_id>/', views.change_department, name='change_department'),
    path('change_password', views.change_password, name='change_password'),
    path('login_change/<int:user_id>/', views.login_change, name='login_change')
]

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from main.scripts import redirect_after_login
from .forms import LoginForm, RegistrationForm, ChangeFirstnameForm, ChangeLastnameForm, ChangeEmailForm
from .forms import ChangeDepartmentForm, ChangePasswordForm
from django.contrib.auth.models import User
from .models import Userprofile
from django.contrib.auth.decorators import login_required


def user_login(request, msg=''):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        nxt = request.POST.get('next')
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect_after_login(nxt)
                else:
                    return render(request, 'account/templates/login.html', {'msg': 'Указанный аккаунт отключен',
                                                                            'form': form})
            else:
                form = LoginForm()
                return render(request, 'account/templates/login.html', {'msg': 'Неверное имя пользователя или '
                                                                                'пароль.Пожалуйста укажите '
                                                                                'корректные данные.',
                                                                        'form': form})
    else:
        form = LoginForm()
    return render(request, 'account/templates/login.html', {'form': form, 'msg': msg})


def create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd['username']).exists():
                return render(request, 'account/templates/registration.html', {"msg": "Такой логин уже существует",
                                                                               'form': form})
            else:
                user = User.objects.create_user(username=cd['username'], password=cd['password'], email=cd['email'],
                                                first_name=cd['first_name'], last_name=cd['last_name'])
                user.save()
                dep = Userprofile.objects.create(user=user, department=cd['department'])
                dep.save()
                return redirect('/account/login', {'msg': 'Пользоватеель успешно зарегестрирован. '
                                                          'Войдите чтобы продолжить'})
    else:
        form = RegistrationForm()
    return render(request, 'account/templates/registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/account/login', {'msg': 'Войдите чтобы продолжить'})


@login_required
def user_profile(request):
    first_name = ChangeFirstnameForm()
    last_name = ChangeLastnameForm()
    email = ChangeEmailForm()
    department = ChangeDepartmentForm()
    return render(request, 'account/templates/user_profile.html', {'first_name': first_name, 'last_name': last_name,
                                                                   'email': email, 'department': department, })


@login_required
def change_first_name(request):
    msg = ''
    user = request.user
    if request.method == 'POST':
        form = ChangeFirstnameForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data['first_name']
            user.first_name = cd
            user.save()
        else:
            msg = 'Необходимо ввести корректные данные'
    return redirect('/account/profile', {'msg': msg})


@login_required
def change_last_name(request):
    msg = ''
    user = request.user
    if request.method == 'POST':
        form = ChangeLastnameForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data['last_name']
            user.last_name = cd
            user.save()
        else:
            msg = 'Необходимо ввести корректные данные'
    return redirect('/account/profile', {'msg': msg})


@login_required
def change_email(request):
    msg = ''
    user = request.user
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data['email']
            user.email = cd
            user.save()
        else:
            msg = 'Необходимо ввести корректные данные'
    return redirect('/account/profile', {'msg': msg})


@login_required
def change_department(request):
    msg = ''
    user = request.user.userprofile
    if request.method == 'POST':
        form = ChangeDepartmentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data['department']
            user.department = cd
            user.save()
        else:
            msg = 'Необходимо ввести корректные данные'
    return redirect('/account/profile', {'msg': msg})


@login_required
def change_password(request):
    u = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = ChangePasswordForm()
        if form.is_valid():
            cd = form.cleaned_data
            old_password = cd["old_password"]
            new_pass = cd["new_pass"]
            new_pass_rep = cd["new_pass_rep"]
            if u.check_password(old_password) and new_pass == new_pass_rep:
                u.set_password(new_pass)
                u.save()
                return redirect('/account/login')
            else:
                return render(request, 'account/templates/change_password.html', {'form': form, 'msg': 'Пароли не '
                                                                                                       'совпадают либо '
                                                                                                       'старый пароль '
                                                                                                       'введен не '
                                                                                                       'верно.'})
    form = ChangePasswordForm()
    return render(request, 'account/templates/change_password.html', {'form': form})

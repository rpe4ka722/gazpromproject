from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from main.models import Department
from main.scripts import redirect_after_login, is_staff
from main.views import structure
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from django.contrib.auth.models import User
from .models import Userprofile
from django.contrib.auth.decorators import login_required


def user_login(request, msg=''):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        nxt = request.POST.get('next')
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            if cd['password'] == '':
                password = '111'
            else:
                password = cd['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active and user.profile.is_password_change:
                    login(request, user)
                    return redirect_after_login(nxt)
                elif user.is_active and user.profile.is_password_change == False:
                    login(request, user)
                    return redirect('account:change_password')
                else:
                    return render(request, 'account/templates/login.html', {'msg': 'Указанный аккаунт отключен',
                                                                            'form': form})
            else:
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
                return redirect('/account/login', {'msg': 'Пользователь успешно зарегестрирован. '
                                                          'Войдите чтобы продолжить'})
    else:
        form = RegistrationForm()
    return render(request, 'account/templates/registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/account/login', {'msg': 'Войдите чтобы продолжить'})


@login_required(login_url='account:login')
@is_staff
def user_detail(request, user_id, msg=''):
    try:
        user = User.objects.get(id=user_id)
        department = Department.objects.all()
        context = {'current_user': user, 'department': department, 'msg': msg}
        return render(request, 'account/templates/user_detail.html', context)
    except ObjectDoesNotExist:
        msg = 'Такого пользователя не существует!'
        return structure(request, msg)


@login_required(login_url='account:login')
def user_profile(request):
    return render(request, 'account/templates/user_profile.html')


@login_required(login_url='account:login')
def change_password(request):
    u = User.objects.get(username=request.user)
    form = ChangePasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            old_password = cd["old_password"]
            new_pass = cd["new_pass"]
            new_pass_rep = cd["new_pass_rep"]
            if u.check_password(old_password) and new_pass == new_pass_rep:
                u.set_password(new_pass)
                u.save()
                profile = u.profile
                profile.is_password_change = True
                profile.save()
                return redirect('account:login')
            else:
                return render(request, 'account/templates/change_password.html', {'form': form, 'msg': 'Пароли не '
                                                                                                       'совпадают либо '
                                                                                                       'старый пароль '
                                                                                                       'введен не '
                                                                                                       'верно.'})
    return render(request, 'account/templates/change_password.html', {'form': form})


@login_required(login_url='account:login')
@is_staff
def login_change(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            login = request.POST['login']
            if User.objects.filter(username=login).exists():
                msg = 'Пользователь с таким именем уже зарегистрирован'
                return user_detail(request, user_id, msg)
            user.username = str(login)
            user.save()
        return user_detail(request, user_id)
    except ObjectDoesNotExist:
        msg = 'Пользователь не найден!'
        return structure(request, msg)


@login_required(login_url='account:login')
@is_staff
def change_first_name(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            firstname = request.POST['firstname']
            user.first_name = str(firstname)
            user.save()
        return user_detail(request, user_id)
    except ObjectDoesNotExist:
        msg = 'Пользователь не найден!'
        return structure(request, msg)


@login_required(login_url='account:login')
@is_staff
def change_last_name(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            lastname = request.POST['lastname']
            user.last_name = str(lastname)
            user.save()
        return user_detail(request, user_id)
    except ObjectDoesNotExist:
        msg = 'Пользователь не найден!'
        return structure(request, msg)


@login_required(login_url='account:login')
@is_staff
def change_department(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            department_id = request.POST['department']
            try:
                department = Department.objects.get(id=department_id)
                user.profile.department = department
                user.profile.save()
            except ObjectDoesNotExist:
                msg = 'Что то пошло не так!'
                return user_detail(request, user_id, msg)
        return user_detail(request, user_id)
    except ObjectDoesNotExist:
        msg = 'Пользователь не найден!'
        return structure(request, msg)


@login_required(login_url='account:login')
@is_staff
def change_email(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            email = request.POST['email']
            user.email = str(email)
            user.save()
        return user_detail(request, user_id)
    except ObjectDoesNotExist:
        msg = 'Пользователь не найден!'
        return structure(request, msg)


@login_required(login_url='account:login')
@is_staff
def password_reset(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            user.set_password('111')
            user.profile.is_password_change = False
            user.save()
            profile = user.profile
            profile.save()
        return user_detail(request, user_id)
    except ObjectDoesNotExist:
        msg = 'Пользователь не найден!'
        return structure(request, msg)
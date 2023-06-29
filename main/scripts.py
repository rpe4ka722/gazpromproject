import pandas as pd
from django.shortcuts import redirect, render

from account.forms import LoginForm
from main.models import Department, Object


def column_dict(name, sheet_name=0, row_number=0):
    data = pd.read_excel(name, sheet_name=sheet_name-1)
    if row_number == 1:
        lst = list(data.columns.values)
    else:
        data = data.iloc[row_number-2]
        lst = [i for i in data]
    dict_col = {i: lst[i] for i in range(len(lst))}
    return dict_col


def str_to_coord(s: str):
    s = s.replace(' ', '')
    print(s)
    print(len(s))
    for i in range(len(s)):
        if s[i].isalpha():
            raise ValueError('Введенные данные некорректны')
    y = s.find('°')
    z = s.find("'")
    a = s.find('"')
    deg = int(s[:y])
    minutes = int(s[y+1:z])
    seconds = s[z+1:a]
    seconds = str(seconds)
    print(seconds)
    seconds = seconds.replace(',', '.')
    print(seconds)
    round(float(seconds), 2)
    result = [deg, minutes, seconds]
    return result


def redirect_after_login(nxt):
    if nxt is None:
        return redirect("main:index")
    else:
        return redirect(nxt)


def is_staff(view_func):
    def decorator(request, *args, **kwargs):
        u = request.user
        if u.is_active and u.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            msg = 'У вас недостаточно прав для данной операции. Обратитесь к администратору либо авторизуйтесь под ' \
                  'другим именем.'
            form = LoginForm
            return render(request, 'account/templates/login.html', {'form': form, 'msg': msg})
    return decorator


def form_errors_text(form):
    error_list = []
    for field in form:
        error_list.append(field.errors.as_text().replace('* ', ''))
    return ' '.join(error_list).strip()


def object_filter(form):
    try:
        ceh = form.data.get('ceh')
        uchastok = form.data.get('uchastok')
        object = form.data.get('object')
        filtered_by = []
        if ceh != '' and ceh is not None:
            department = Department.objects.filter(ceh=ceh, is_prod=True)
            objects = Object.objects.filter(uchastok__in=department)
            filtered_by.append(ceh)
        elif uchastok != '' and uchastok is not None:
            department = Department.objects.filter(uchastok=uchastok, is_prod=True)
            objects = Object.objects.filter(uchastok__in=department)
            filtered_by.append(uchastok)
        elif object != '' and object is not None:
            objects = Object.objects.filter(object_name__contains=object)
            [filtered_by.append(str(i.object_name)) for i in objects]
        else:
            objects = Object.objects.all()
        return objects, filtered_by
    except (ValueError, TypeError):
        pass

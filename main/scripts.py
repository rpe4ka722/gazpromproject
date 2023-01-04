import pandas as pd
from django.shortcuts import redirect, render

from account.forms import LoginForm


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

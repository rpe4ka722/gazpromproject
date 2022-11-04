from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Введите ваш логин', max_length=20,
                               widget=forms.TextInput(attrs={'class': 'account-forms'}))
    password = forms.CharField(label='Введите ваш пароль', max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'account-forms'}))


class RegistrationForm(forms.Form):
    DEPARTMENT_CHOICES = [
        ('Администрация', 'Администрация'),
        ('Сургутский цех связи', 'Сургутский цех связи'),
        ('Ноябрьский цех связи', 'Ноябрьский цех связи'),
        ('Тюменский цех связи', 'Тюменский цех связи'),
        ('Производственная лаборатория связи', 'Производственная лаборатория связи'),
    ]

    username = forms.CharField(label='Введите ваш логин', max_length=20,
                               widget=forms.TextInput(attrs={'class': 'account-forms'}))
    password = forms.CharField(label='Введите ваш пароль', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'account-forms'}))
    first_name = forms.CharField(label='Введите ваше имя', max_length=20,
                                 widget=forms.TextInput(attrs={'class': 'account-forms'}))
    last_name = forms.CharField(label='Введите вашу фамилию', max_length=20,
                                widget=forms.TextInput(attrs={'class': 'account-forms'}))
    email = forms.EmailField(label='Введите ваш e-mail', widget=forms.EmailInput(attrs={'class': 'account-forms'}))
    department = forms.ChoiceField(label='Выберите ваше подразделение', choices=DEPARTMENT_CHOICES,
                                   widget=forms.Select(attrs={'class': 'account-forms'}))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Введите старый пароль', max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'account-forms'}))
    new_pass = forms.CharField(label='Введите новый пароль', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'account-forms'}))
    new_pass_rep = forms.CharField(label='Введите новый пароль', max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'account-forms'}))


class ChangeFirstnameForm(forms.Form):
    first_name = forms.CharField(label='Введите новое имя', max_length=20,
                                 widget=forms.TextInput(attrs={'class': 'account-forms'}))


class ChangeLastnameForm(forms.Form):
    last_name = forms.CharField(label='Введите новую фамилию', max_length=20,
                                widget=forms.TextInput(attrs={'class': 'account-forms'}))


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='Введите новый e-mail', widget=forms.EmailInput(attrs={'class': 'account-forms'}))


class ChangeDepartmentForm(forms.Form):
    DEPARTMENT_CHOICES = [
        ('Администрация', 'Администрация'),
        ('Сургутский цех связи', 'Сургутский цех связи'),
        ('Ноябрьский цех связи', 'Ноябрьский цех связи'),
        ('Тюменский цех связи', 'Тюменский цех связи'),
        ('Производственная лаборатория связи', 'Производственная лаборатория связи'),
    ]
    department = forms.ChoiceField(label='Выберите ваше подразделение', choices=DEPARTMENT_CHOICES,
                                   widget=forms.Select(attrs={'class': 'account-forms'}))

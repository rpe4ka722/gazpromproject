from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from main.models import Department


class LoginForm(forms.Form):
    username = forms.CharField(label='Введите ваш логин', max_length=20,
                               widget=forms.TextInput(attrs={'class': 'account-forms'}))
    password = forms.CharField(label='Введите ваш пароль', max_length=50, required=False,
                               widget=forms.PasswordInput(attrs={'class': 'account-forms'}))


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email',
                  'is_staff']
        help_texts = {
            'username': _(''),
            'is_staff': _('Отметьте если пользователь имеет права администратора'),
        }


class UserCreationForm(RegistrationForm, forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='', label='Укажите подразделение')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Введите старый пароль', max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'account-forms'}))
    new_pass = forms.CharField(label='Введите новый пароль', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'account-forms'}))
    new_pass_rep = forms.CharField(label='Введите новый пароль', max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'account-forms'}))

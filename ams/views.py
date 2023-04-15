from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from ams.forms import AmsForm
from ams.models import Ams
from main.scripts import form_errors_text


def ams(request):
    object_list = Ams.objects.all()
    context = {'object': object_list}
    return render(request, 'ams/templates/ams_list.html', context)


def ams_create(request):
    form = AmsForm(request.POST or None)
    msg = ''
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('ams:ams')
        else:
            msg = form_errors_text(form)
    context = {'form': form, 'msg': msg}
    return render(request, 'ams/templates/ams_creation.html', context)


def export_xls_ams(request):
    pass


def delete_ams(request, ams_id):
    pass


def ams_detail(request, ams_id):
    msg = ''
    try:
        ams_object = Ams.objects.get(id=ams_id)
    except ObjectDoesNotExist:
        msg = 'Такой АМС не существует'
    context = {'i': ams_object, 'msg': msg}
    return render(request, 'ams/templates/ams_details.html', context)
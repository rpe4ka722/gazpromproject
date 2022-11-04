from datetime import datetime
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ObjectForm, RrlForm, PositionForm, UploadXlsForm, UploadChoiceForm, ImportForm, DepartmentForm, \
    EmployeeForm
from .models import Object, Position, RrlLine, Sheet, Header, UploadedData, Choice, Department, Employee, Ozp, \
    Foto_zamechanya, Foto_vipolnenya
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Border, Side, Alignment, Font

from .scripts import str_to_coord


def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/templates/index.html')
    else:
        return redirect('/account/login')


def object_index(request):
    if request.user.is_authenticated:
        return render(request, 'main/templates/object_index.html')
    else:
        return redirect('/account/login')


def create_object(request):
    if request.method == 'POST':
        obj_form = ObjectForm(request.POST)
        pos_form = PositionForm(request.POST)
        if obj_form.is_valid() and pos_form.is_valid():
            cd_obj = obj_form.cleaned_data
            cd_pos = pos_form.cleaned_data
            pos = Position(latitude_degrees=cd_pos['latitude_degrees'],
                           latitude_minutes=cd_pos['latitude_minutes'], latitude_seconds=cd_pos['latitude_seconds'],
                           longitude_degrees=cd_pos['longitude_degrees'], longitude_minutes=cd_pos['longitude_minutes'],
                           longitude_seconds=cd_pos['longitude_seconds'], address=cd_pos['address'],
                           district=cd_pos['district'])
            pos.save()
            user = request.user
            time = datetime.now()
            obj = Object(object_name=cd_obj['object_name'], position=pos, rrl_line=cd_obj['rrl_line'],
                         uchastok=cd_obj['uchastok'], last_modify=user, time_modify=time)
            obj.save()
            return redirect('/')
        else:
            msg = 'Введенные данные некорректны'
            return render(request, "main/templates/object_creation.html", {'obj_form': obj_form,
                                                                           'pos_form': pos_form, 'msg': msg})

    else:
        obj_form = ObjectForm()
        pos_form = PositionForm()
    return render(request, "main/templates/object_creation.html", {'obj_form': obj_form, 'pos_form': pos_form})


def create_rrl(request):
    if request.method == 'POST':
        form = RrlForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            rrl = RrlLine(rrl_line_name=cd['rrl_line_name'], station_count=cd['station_count'],
                          bandwidth=cd['bandwidth'])
            rrl.save()
            return redirect('main:rrl_line')
        else:
            msg = 'Вы ввели некорректные данные'
            context = {'form': form, 'msg': msg}
            return render(request, "main/templates/rrl_creation.html", context)
    else:
        form = RrlForm()
    return render(request, "main/templates/rrl_creation.html", {'form': form})


def objects_list(request):
    objectslist = Object.objects.all()
    position = Position.objects.all()
    context = {'objectlist': objectslist, 'position': position}
    return render(request, 'main/templates/objects.html', context)


def object_detail(request, name):
    selected_object = Object.objects.get(id=name)
    full_name = selected_object.last_modify.first_name + ' ' + selected_object.last_modify.last_name
    context = {'name': selected_object.object_name, 'user': str(full_name), 'time': selected_object.time_modify}
    return render(request, 'main/templates/object_detail.html', context)


def upload_xls(request):
    if request.method == 'POST':
        form = UploadXlsForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            object_id = file.id
            sheets = file.sheets()
            for i in sheets:
                inst = Sheet(sheet_name=i)
                inst.save()
            return redirect(reverse('main:upload_choice', kwargs={'object_id': object_id}))
    else:
        form = UploadXlsForm()
    return render(request, "main/templates/upload.html", {'form': form})


def upload_choice(request, object_id):
    if request.method == 'POST':
        form = UploadChoiceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            instance = Choice(sheet=cd['sheet'], row=cd['row'])
            instance.save()
            sheet = instance.sheet
            row = instance.row
            data = UploadedData.objects.get(id=object_id)
            headers_list = data.headers(sheet, row)
            for i in headers_list:
                x = Header(header=i)
                x.save()
            return redirect(reverse('main:import_data', kwargs={'choice': instance.id, 'object_id': object_id}))
    else:
        form = UploadChoiceForm()
    return render(request, "main/templates/upload_1.html", {'form': form, 'object_id': object_id})


def import_data(request, choice, object_id):
    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            object_name = Header.objects.get(header=cd['object_name'])
            coords_lat = Header.objects.get(header=cd['coords_lat'])
            coords_lon = Header.objects.get(header=cd['coords_lon'])
            district = Header.objects.get(header=cd['district'])
            address = Header.objects.get(header=cd['address'])
            choice = Choice.objects.get(id=choice)
            choice.object_name = object_name
            choice.coords_lat = coords_lat
            choice.coords_lon = coords_lon
            choice.district = district
            choice.address = address
            choice.save()
            data = UploadedData.objects.get(id=object_id)
            wb = load_workbook(filename=data.file)
            sheet_name = str(choice.sheet.sheet_name)
            ws = wb[sheet_name]
            row_count = ws.max_row
            x: dict = {}
            for cols in ws.iter_cols(min_row=choice.row, max_row=choice.row):
                for cell in cols:
                    if str(cell.value) == str(choice.object_name):
                        x.update({'object_name': cell.column})
                    if str(cell.value) == str(choice.coords_lat):
                        x.update({'coords_lat': cell.column})
                    if str(cell.value) == str(choice.coords_lon):
                        x.update({'coords_lon': cell.column})
                    if str(cell.value) == str(choice.district):
                        x.update({'district': cell.column})
                    if str(cell.value) == str(choice.address):
                        x.update({'address': cell.column})
            print(x)
            for row in range(row_count):
                lat = ws.cell(row=row+5, column=x['coords_lat']).value
                lon = ws.cell(row=row+5, column=x['coords_lon']).value
                if lat is None or lon is None:
                    pass
                else:
                    y = str_to_coord(lat)
                    print(y)
                    z = str_to_coord(lon)
                    print(z)
                    pos = Position(latitude_degrees=y[0], latitude_minutes=y[1], latitude_seconds=y[2],
                                   longitude_degrees=z[0], longitude_minutes=z[1], longitude_seconds=z[2],
                                   address=ws.cell(row=row+5, column=x['address']).value,
                                   district=ws.cell(row=row+5, column=x['district']).value)
                    print(pos.address)
                    pos.save()
                    user = request.user
                    time = datetime.now()
                    obj = Object(object_name=ws.cell(row=row+5, column=x['object_name']).value, position=pos,
                                 last_modify=user, time_modify=time)
                    obj.save()
            for i in Header.objects.all():
                i.delete()
            for i in Choice.objects.all():
                i.delete()
            for i in Sheet.objects.all():
                i.delete()
            for i in UploadedData.objects.all():
                i.delete()
            return redirect('main:objects')

    else:
        form = ImportForm()
    return render(request, "main/templates/import.html", {'form': form, 'choice': choice, 'object_id': object_id})


def structure(request):
    if request.GET:
        objectslist = Department.objects.filter(ceh__exact=request.GET['ceh'])
        if request.GET['ceh'] == '':
            filtered_by = 'Отсутствует'
        else:
            filtered_by = request.GET['ceh']
    else:
        objectslist = Department.objects.all()
        filtered_by = 'all'
    ceh_list = []
    for i in Department.objects.all():
        if i.ceh in ceh_list:
            pass
        else:
            ceh_list.append(i.ceh)

    employee = Employee.objects.all()
    context = {'objectlist': objectslist, 'employee': employee, 'ceh': ceh_list, 'filtered_by': filtered_by}
    return render(request, "main/templates/structure.html",  context)


def create_uchastok(request):
    if request.method == 'POST':
        form1 = DepartmentForm(request.POST)
        form2 = EmployeeForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            cd1 = form1.cleaned_data
            cd2 = form2.cleaned_data
            dep = Department(ceh=cd1['ceh'], uchastok=cd1['uchastok'])
            dep.save()
            emp = Employee(employee_name=cd2['employee_name'], employee_last_name=cd2['employee_last_name'],
                           uchastok_instance=dep)
            emp.save()
            return redirect('main:structure')
        else:
            msg = 'Вы ввели некорректные данные'
            context = {'form1': form1, 'form2': form2, 'msg': msg}
            return render(request, "main/templates/uchastok_creation.html", context)
    else:
        form1 = DepartmentForm()
        form2 = EmployeeForm()
        context = {'form1': form1, 'form2': form2}
    return render(request, "main/templates/uchastok_creation.html", context)


def delete_uchastok(request, pk):
    try:
        obj = Department.objects.get(id=pk)
        obj.delete()
        return redirect('main:structure')
    except Department.DoesNotExist:
        return HttpResponseNotFound("<h2>Not found</h2>")


def change_uchastok(request, pk):
    obj = Employee.objects.get(id=pk)
    uch = obj.uchastok_instance.uchastok
    name = str(obj.employee_name + ' ' + obj.employee_last_name)
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj.employee_name = cd['employee_name']
            obj.employee_last_name = cd['employee_last_name']
            obj.save()
            return redirect('main:structure')
        else:
            msg = 'Вы ввели некорректные данные'
            context = {'form': form, 'msg': msg, 'pk': pk, 'uch': uch, 'name': name}
            return render(request, "main/templates/change_uchastok.html", context)
    else:
        form = EmployeeForm()
        context = {'form': form, 'pk': pk, 'uch': uch, 'name': name}
    return render(request, "main/templates/change_uchastok.html", context)


def export_xls_department(request, ceh):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="dep.xlsx"'
    wb = Workbook()
    ws = wb.active
    row_num = 1
    columns = ['Цех', 'Участок', 'Начальник участка']
    font = Font(name='TimesNewRoman', sz=11, bold=True)
    font2 = Font(name='TimesNewRoman', sz=11, bold=False)
    border = Border(left=Side(border_style='thin', color='FF000000'),
                    right=Side(border_style='thin', color='FF000000'),
                    top=Side(border_style='thin', color='FF000000'),
                    bottom=Side(border_style='thin', color='FF000000'))
    alignment = Alignment(horizontal='center',
                          vertical='center',
                          text_rotation=0,
                          wrap_text=True,
                          shrink_to_fit=False,
                          indent=0)
    for col_num in range(len(columns)):
        ws.cell(row_num, col_num+1, columns[col_num])
        ws.cell(row_num, col_num+1).font = font
        ws.cell(row_num, col_num + 1).border = border
        ws.cell(row_num, col_num + 1).alignment = alignment
    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 30
    if ceh == 'all':
        rows = Department.objects.all()
    elif ceh == 'Отсутствует':
        rows = Department.objects.filter(ceh__exact='')
    else:
        rows = Department.objects.filter(ceh__exact=ceh)
    for row in range(rows.count()):
        atr_list = [rows[row].ceh, rows[row].uchastok, rows[row].employee.employee_name + ' ' +
                    rows[row].employee.employee_last_name]
        for col_num in range(len(atr_list)):
            ws.cell(row+2, col_num+1, atr_list[col_num])
            ws.cell(row + 2, col_num + 1).font = font2
            ws.cell(row + 2, col_num + 1).border = border
            ws.cell(row + 2, col_num + 1).alignment = alignment
    wb.save(response)
    return response


def rrl_line(request):
    objectslist = RrlLine.objects.all()
    context = {'objectlist': objectslist}
    return render(request, "main/templates/rrl.html", context)


def export_rrl(requst):
    pass


def delete_rrl(request, pk):
    try:
        obj = RrlLine.objects.get(id=pk)
        obj.delete()
        return redirect('main:rrl_line')
    except Department.DoesNotExist:
        return HttpResponseNotFound("<h2>Not found</h2>")


def change_rrl(request, pk):
    obj = RrlLine.objects.get(id=pk)
    if request.method == 'POST':
        form = RrlForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj.rrl_line_name = cd['rrl_line_name']
            obj.station_count = cd['station_count']
            obj.bandwidth = cd['bandwidth']
            obj.save()
            return redirect('main:rrl_line')
        else:
            msg = 'Вы ввели некорректные данные'
            context = {'form': form, 'msg': msg, 'pk': pk, 'obj': obj}
            return render(request, "main/templates/change_rrl.html", context)
    else:
        form = RrlForm()
        context = {'form': form, 'pk': pk, 'obj': obj}
    return render(request, "main/templates/change_rrl.html", context)


def export_objects(request):
    pass


def change_object(request, pk):
    try:
        obj = Object.objects.get(id=pk)
    except Department.DoesNotExist:
        return HttpResponseNotFound("<h2>Not found</h2>")
    if request.method == 'POST':
        obj_form = ObjectForm(request.POST)
        pos_form = PositionForm(request.POST)
        if obj_form.is_valid() and pos_form.is_valid():
            cd_obj = obj_form.cleaned_data
            cd_pos = pos_form.cleaned_data
            pos = Position(latitude_degrees=cd_pos['latitude_degrees'],
                           latitude_minutes=cd_pos['latitude_minutes'], latitude_seconds=cd_pos['latitude_seconds'],
                           longitude_degrees=cd_pos['longitude_degrees'], longitude_minutes=cd_pos['longitude_minutes'],
                           longitude_seconds=cd_pos['longitude_seconds'], address=cd_pos['address'],
                           district=cd_pos['district'])
            pos.save()
            user = request.user
            time = datetime.now()
            obj = Object(object_name=cd_obj['object_name'], position=pos, rrl_line=cd_obj['rrl_line'],
                         uchastok=cd_obj['uchastok'], last_modify=user, time_modify=time)
            obj.save()
            return redirect('/')
        else:
            msg = 'Введенные данные некорректны'
            return render(request, "main/templates/object_creation.html", {'obj_form': obj_form,
                                                                           'pos_form': pos_form, 'msg': msg})



def delete_object(reqest, pk):
    try:
        obj = Object.objects.get(id=pk)
        obj.delete()
        return redirect('main:objects')
    except Department.DoesNotExist:
        return HttpResponseNotFound("<h2>Not found</h2>")


def ozp_create(request):
    objects = Object.objects.all()
    if request.method == 'POST':
        uploaded_file = request.FILES['foto_do']
        accepted_list = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
        name = str(uploaded_file.name)
        associated_object = request.POST['associated_object']
        print(associated_object)
        zamechanie_ozp = str(request.POST['zamechanie_ozp'])
        normative_documentation = str(request.POST['normative_documentation'])
        if name.endswith(accepted_list):
            x = Ozp.objects.create(object_name=Object.objects.get(object_name=associated_object),
                                   zamechanie_ozp=zamechanie_ozp, normative_documentation=normative_documentation,
                                   last_modify=request.user)
            x.save()
            y = Foto_zamechanya.objects.create(zamechanie=x, foto=uploaded_file)
            y.save()
            return redirect("main:ozp")
        else:
            msg = 'Загружать необходимо файл изображения!'
            context = {'objects': objects, 'msg': msg}
            return render(request, "main/templates/ozp_creation.html", context)
    context = {'objects': objects}
    return render(request, "main/templates/ozp_creation.html", context)


def ozp(request):
    objectslist = Ozp.objects.all()
    context = {'objectlist': objectslist}
    return render(request, "main/templates/ozp.html", context)


def ozp_details(request, ozp_id):
    ozp_object = Ozp.objects.get(id=ozp_id)
    foto_do = Foto_zamechanya.objects.filter(zamechanie=ozp_object)
    posle_foto = Foto_vipolnenya.objects.filter(zamechanie=ozp_object)
    context = {'i': ozp_object, 'foto_do': foto_do, 'posle_foto': posle_foto}
    return render(request, "main/templates/ozp_details.html", context)


def ozp_zamechanie_change(request, ozp_id):
    object = Ozp.objects.get(id=ozp_id)
    if request.method == 'POST':
        zamechanie = request.POST['text_zamechanya']
        object.zamechanie_ozp = str(zamechanie)
        object.save()
    return redirect('main:ozp_details', ozp_id=ozp_id)


def ozp_normative_change(request, ozp_id):
    object = Ozp.objects.get(id=ozp_id)
    if request.method == 'POST':
        normative = request.POST['text_normative']
        object.normative_documentation = str(normative)
        object.save()
    return redirect('main:ozp_details', ozp_id=ozp_id)


def srok_ustranenia_change(request, ozp_id):
    object = Ozp.objects.get(id=ozp_id)
    if request.method == 'POST':
        srok = request.POST['srok']
        if srok:
            object.zakrytie_date = srok
            object.save()
    return redirect('main:ozp_details', ozp_id=ozp_id)


def control_srok_change(request, ozp_id):
    object = Ozp.objects.get(id=ozp_id)
    if request.method == 'POST':
        srok = request.POST['srok']
        if srok:
            object.control_date = srok
            object.save()
    return redirect('main:ozp_details', ozp_id=ozp_id)


def foto_zamechanie_add(request, ozp_id):
    object = Ozp.objects.get(id=ozp_id)
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['foto']
            x = Foto_zamechanya.objects.create(zamechanie=object, foto=uploaded_file)
            x.save()
        except KeyError:
            pass
    return redirect('main:ozp_details', ozp_id=ozp_id)


def foto_do_delete(request, f_id):
    x = Foto_zamechanya.objects.get(id=f_id)
    ozp_id = x.zamechanie.id
    x.delete()
    return redirect('main:ozp_details', ozp_id=ozp_id)


def posle_foto_delete(request, f_id):
    x = Foto_vipolnenya.objects.get(id=f_id)
    ozp_id = x.zamechanie.id
    x.delete()
    return redirect('main:ozp_details', ozp_id=ozp_id)


def foto_vipolnenie_add(request, ozp_id):
    object = Ozp.objects.get(id=ozp_id)
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['foto']
            x = Foto_vipolnenya.objects.create(zamechanie=object, foto=uploaded_file)
            x.save()
        except KeyError:
            pass
    return redirect('main:ozp_details', ozp_id=ozp_id)


def accept(request, ozp_id):
    object = Ozp.objects.get(id=ozp_id)
    object.is_done = True
    object.save()
    return redirect('main:ozp_details', ozp_id=ozp_id)
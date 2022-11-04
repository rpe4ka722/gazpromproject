from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('objects', views.objects_list, name='objects'),
    path('object_index', views.object_index, name='object_index'),
    path('create_object', views.create_object, name='create_object'),
    path('create_rrl', views.create_rrl, name='create_rrl'),
    path('objects/<name>', views.object_detail, name='object_detail'),
    path('upload', views.upload_xls, name='upload_xls'),
    path('upload_choice/<object_id>', views.upload_choice, name='upload_choice'),
    path('import_data/<choice>/<int:object_id>', views.import_data, name='import_data'),
    path('structure', views.structure, name='structure'),
    path('create_uchastok', views.create_uchastok, name='create_uchastok'),
    path('delete_uchastok/<int:pk>', views.delete_uchastok, name='delete_uchastok'),
    path('change_uchastok/<int:pk>', views.change_uchastok, name='change_uchastok'),
    path('export_xls_department/<ceh>', views.export_xls_department, name='export_xls_department'),
    path('rrl_line', views.rrl_line, name='rrl_line'),
    path('export_rrl', views.export_rrl, name='export_rrl'),
    path('change_rrl/<int:pk>', views.change_rrl, name='change_rrl'),
    path('delete_rrl/<int:pk>', views.delete_rrl, name='delete_rrl'),
    path('export_objects', views.export_objects, name='export_objects'),
    path('delete_object/<int:pk>', views.delete_object, name='delete_object'),
    path('change_object/<int:pk>', views.change_object, name='change_object'),
    path('ozp_create', views.ozp_create, name='ozp_create'),
    path('ozp', views.ozp, name='ozp'),
    path('ozp_details/<int:ozp_id>', views.ozp_details, name='ozp_details'),
    path('ozp_zamechanie_change/<int:ozp_id>', views.ozp_zamechanie_change, name='ozp_zamechanie_change'),
    path('ozp_normative_change/<int:ozp_id>', views.ozp_normative_change, name='ozp_normative_change'),
    path('srok_ustranenia_change/<int:ozp_id>', views.srok_ustranenia_change, name='srok_ustranenia_change'),
    path('control_srok_change/<int:ozp_id>', views.control_srok_change, name='control_srok_change'),
    path('foto_zamechanie_add/<int:ozp_id>', views.foto_zamechanie_add, name='foto_zamechanie_add'),
    path('foto_do_delete/<int:f_id>', views.foto_do_delete, name='foto_do_delete'),
    path('posle_foto_delete/<int:f_id>', views.posle_foto_delete, name='posle_foto_delete'),
    path('foto_vipolnenie_add/<int:ozp_id>', views.foto_vipolnenie_add, name='foto_vipolnenie_add'),
    path('accept/<int:ozp_id>', views.accept, name='accept')
    ]
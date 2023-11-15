from django.urls import path
from .views import searchdoc, index, sertifikat, bpkb_mobil_dan_motor, pdfupload, pdfdownload, pdfremove, export, update, add, delete, authorization_rejected

prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='searchdoc', view=searchdoc, name=prefix + 'searchdoc'),
    path(route='', view=index, name=prefix + 'index'),
    path(route='sertifikat', view=sertifikat, name=prefix + 'sertifikat'),
    path(route='bpkb_mobil_dan_motor', view=bpkb_mobil_dan_motor, name=prefix + 'bpkb_mobil_dan_motor'),
    path(route='pdfupload/<str:uuid_id>', view=pdfupload, name=prefix + 'pdfupload'),
    path(route='pdfdownload/<str:uuid_id>', view=pdfdownload, name=prefix + 'pdfdownload'),
    path(route='pdfremove/<str:uuid_id>', view=pdfremove, name=prefix + 'pdfremove'),
    path(route='delete/<str:uuid_id>', view=delete, name=prefix + 'delete'),
    path(route='export', view=export, name=prefix + 'export'),
    path(route='add', view=add, name=prefix + 'add'),
    path(route='update/<str:uuid_id>', view=update, name=prefix + 'update'),
    path(route='authorization_rejected', view=authorization_rejected, name=prefix + 'authorization_rejected'),


]
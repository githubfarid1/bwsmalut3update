from django.urls import path
from .views import irigasi, pdfdownload, air_baku, sungai, pantai, keuangan, statistics, boxsearch, pdfupload, pdfremove, searchdoc, export
#tes2, tes1
prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='irigasi', view=irigasi, name=prefix + "irigasi"),
    path(route='air_baku', view=air_baku, name=prefix + "air_baku"),
    path(route='pantai', view=pantai, name=prefix + "pantai"),
    path(route='sungai', view=sungai, name=prefix + "sungai"),
    path(route='keuangan', view=keuangan, name=prefix + "keuangan"),
    path(route='pdfdownload/<str:uuid_id>', view=pdfdownload, name=prefix + 'pdfdownload'),
    path(route='', view=statistics, name=prefix + "statistics"),
    # path(route='boxsearch/<str:link>/<str:box_number>', view=boxsearch, name=prefix + 'boxsearch'),
    path(route='boxsearch', view=boxsearch, name=prefix + 'boxsearch'),
    path(route='pdfupload/<str:uuid_id>', view=pdfupload, name=prefix + 'pdfupload'),
    path(route='pdfremove/<str:uuid_id>', view=pdfremove, name=prefix + 'pdfremove'),
    path(route='searchdoc', view=searchdoc, name=prefix + 'searchdoc'),
    path(route='export', view=export, name=prefix + 'export'),
    

]
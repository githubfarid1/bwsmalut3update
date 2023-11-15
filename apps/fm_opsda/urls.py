from django.urls import path
from .views import add_department, department, department_year, page_404, department_list, showfolder, download
prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='add_department', view=add_department, name=prefix + "add_department"),
    path(route='department/<str:slug>', view=department, name=prefix + "department"),
    path(route='department_year/<str:slug>/<int:year>', view=department_year, name=prefix + "department_year"),
    path(route='page_404', view=page_404, name=prefix + "page_404"),
    path(route='department_list', view=department_list, name=prefix + "department_list"),
    path(route='showfolder/<str:slug>/<str:year>', view=showfolder, name=prefix + "showfolder"),
    path(route='download/<str:slug>/<str:year>', view=download, name=prefix + 'download'),
]
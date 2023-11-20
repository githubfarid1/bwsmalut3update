from django.urls import path
from .views import add_department, department, page_404, department_list, download, folder_list, show_folder, add_folder, upload_file, remove_file, download_folder,  rename_file
prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='add_department', view=add_department, name=prefix + "add_department"),
    path(route='department/<str:slug>', view=department, name=prefix + "department"),
    path(route='page_404', view=page_404, name=prefix + "page_404"),
    path(route='department_list', view=department_list, name=prefix + "department_list"),
    path(route='download/<str:slug>/<str:year>', view=download, name=prefix + 'download'),
    path(route='folder_list', view=folder_list, name=prefix + "folder_list"),
    path(route='show_folder/<str:slug>/<str:year>', view=show_folder, name=prefix + "show_folder"),
    path(route='add_folder', view=add_folder, name=prefix + "add_folder"),
    path(route='upload_file', view=upload_file, name=prefix + "upload_file"),
    path(route='remove_file', view=remove_file, name=prefix + "remove_file"),
    path(route='download_folder', view=download_folder, name=prefix + "download_folder"),
    path(route='rename_file', view=rename_file, name=prefix + "rename_file"),

]
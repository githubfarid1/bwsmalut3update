from django.urls import path
from .views import (
    DepartmentView,
    DepartmentListView,
    AddDepartmentView,
    FolderListView,
    ShowFolderView,
    AddFolderView,
    UploadFileView,
    RemoveFileView,
    DownloadView,
    DownloadFolderView,
    RenameFileView,
    Page404View,
)
app_name = 'apps.fm_balai'  # adjust to your app name

urlpatterns = [
    path('add_department', AddDepartmentView.as_view(), name='fm_balai_add_department'),
    path('department/<str:slug>/', DepartmentView.as_view(), name='fm_balai_department'),
    path('page_404/', Page404View.as_view(), name='fm_balai_page_404'),
    path('department_list', DepartmentListView.as_view(), name='fm_balai_department_list'),
    path('download/<str:slug>/<str:year>/', DownloadView.as_view(), name='fm_balai_download'),
    path('folder_list', FolderListView.as_view(), name='fm_balai_folder_list'),
    path('show_folder/<str:slug>/<str:year>/', ShowFolderView.as_view(), name='fm_balai_show_folder'),
    path('add_folder', AddFolderView.as_view(), name='fm_balai_add_folder'),
    path('upload_file', UploadFileView.as_view(), name='fm_balai_upload_file'),
    path('remove_file', RemoveFileView.as_view(), name='fm_balai_remove_file'),
    path('download_folder', DownloadFolderView.as_view(), name='fm_balai_download_folder'),
    path('rename_file', RenameFileView.as_view(), name='fm_balai_rename_file'),
]
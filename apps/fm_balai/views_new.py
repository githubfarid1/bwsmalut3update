from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils import timezone

from .models import Department
from .forms import DepartmentForm, AddFolderForm, RenameFileForm

import os
import shutil
import json
import mimetypes
from datetime import date, datetime


def check_permission(user, depslug):
    if user.is_superuser:
        return True
    if depslug == '':
        groupname = __package__.split('.')[1]
    else:
        groupname = __package__.split('.')[1] + "_" + depslug

    test_group1 = Group.objects.get(name=__package__.split('.')[1])
    test_group2 = Group.objects.get(name=groupname)
    user_group = user.groups.all()
    if test_group1 in user_group:
        return True
    if test_group2 in user_group:
        return True
    return False


def checkfolder(path):
    contents = os.listdir(path)
    if len(contents) == 0:
        return False

    for file in contents:
        if os.path.isdir(os.path.join(path, file)):
            condirs = os.listdir(os.path.join(path, file))
            if len(condirs) != 0:
                return True
    return False


def get_fileinfo(filepath):
    file_size = os.path.getsize(filepath)
    unit = 'bytes'
    if file_size < 90000000:
        unit = 'kb'
    elif file_size < 900000000:
        unit = 'mb'
    elif file_size < 9000000000:
        unit = 'gb'

    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    size = file_size / 1024 ** exponents_map[unit]
    file_size_rounded = round(size, 2)

    filesizestr = f"{file_size_rounded} {unit}"

    mime_type, encoding = mimetypes.guess_type(filepath)

    mtime = os.path.getmtime(filepath)

    if mime_type:
        if 'pdf' in mime_type:
            filemime, filetype = 'pdf.png', 'PDF'
        elif 'excel' in mime_type or 'sheet' in mime_type:
            filemime, filetype = 'excel.png', 'Excel'
        elif 'png' in mime_type or 'jpg' in mime_type or 'jpeg' in mime_type:
            filemime, filetype = 'image.png', 'Image'
        elif 'mp3' in mime_type:
            filemime, filetype = 'sound.png', 'Sound'
        elif 'video' in mime_type:
            filemime, filetype = 'video.png', 'Video'
        elif 'powerpoint' in mime_type or 'presentation' in mime_type:
            filemime, filetype = 'ppt.png', 'Power Point'
        elif 'wordprocessingml' in mime_type or 'msword' in mime_type:
            filemime, filetype = 'doc.png', 'Word'
        elif 'compressed' in mime_type or 'zip' in mime_type:
            filemime, filetype = 'zip.png', 'Zip'
        else:
            filemime, filetype = 'unknown.png', 'Unknown'
    else:
        filemime, filetype = 'unknown.png', 'Unknown'

    return filemime, filesizestr, filetype, mime_type, mtime


def build_breadcrumbs(url):
    folderlist = str(url).split(os.path.sep)
    result = []
    for idx, folder in enumerate(folderlist):
        tmpl = folderlist[:idx + 1]
        mdict = {
            'label': folder,
            'link': os.path.sep.join(tmpl),
        }
        result.append(mdict)
    if result:
        result[-1]['link'] = ''
    return result


@method_decorator(csrf_exempt, name='dispatch')
class DepartmentView(View):
    def get(self, request, slug):
        if not request.user.is_authenticated:
            return redirect('login')

        if not check_permission(request.user, slug):
            return render(request, 'file_manager/page_404.html', {'message': 'Otorisasi Ditolak'})

        dep = Department.objects.filter(slug=slug).first()
        if not dep:
            return render(request, 'file_manager/page_404.html', {'message': 'Halaman tidak ada'})

        path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug)
        contents = os.listdir(path)

        context = {
            "years": contents,
            'depname': dep.name,
            'slug': slug,
            'satkername': 'BALAI',
            'depurl': 'fm_balai_department',
            'deplisturl': 'fm_balai_department_list',
            'depyearurl': 'fm_balai_department_year',
            'showfolderurl': 'fm_balai_show_folder',
        }
        return render(request, 'file_manager/department.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class DepartmentListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        departments = Department.objects.all()
        data = [{'name': dep.name, 'create_date': dep.create_date, 'slug': dep.slug} for dep in departments]

        context = {
            'data': data,
            'satkername': 'BALAI',
            'depurl': 'fm_balai_department',
        }
        return render(request, 'file_manager/department_list.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class AddDepartmentView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if not check_permission(request.user, ''):
            return render(request, 'file_manager/page_404.html', {'message': 'Otorisasi Ditolak'})

        departments = Department.objects.all()
        data = [{'name': dep.name, 'create_date': dep.create_date, 'slug': dep.slug} for dep in departments]

        form = DepartmentForm()
        context = {
            'data': data,
            'satkername': 'BALAI',
            'depurl': 'fm_balai_department',
            'form': form,
        }
        return render(request, 'file_manager/add_department.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if not check_permission(request.user, ''):
            return render(request, 'file_manager/page_404.html', {'message': 'Otorisasi Ditolak'})

        departments = Department.objects.all()
        data = [{'name': dep.name, 'create_date': dep.create_date, 'slug': dep.slug} for dep in departments]

        if request.POST.get('slug'):
            dep = get_object_or_404(Department, slug=request.POST['slug'])
            folder_path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], dep.folder)
            if checkfolder(folder_path):
                messages.info(request, "Tidak bisa dihapus karena ada folder terhubung")
                return redirect(request.build_absolute_uri())
            else:
                dep.delete()
                shutil.rmtree(folder_path)
                messages.info(request, "Hapus PPK Berhasil")
                return redirect(request.build_absolute_uri())

        form = DepartmentForm(request.POST)
        if form.is_valid():
            newdep = form.save(commit=False)
            foldertmp = newdep.shortname.lower().replace(' ', '-')
            if not os.path.exists(os.path.join(settings.FM_LOCATION, __package__.split('.')[1])):
                os.mkdir(os.path.join(settings.FM_LOCATION, __package__.split('.')[1]))

            folder = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], foldertmp)
            if not os.path.exists(folder):
                os.mkdir(folder)
                today = date.today()
                os.mkdir(os.path.join(folder, str(today.year)))
                os.mkdir(os.path.join(folder, str(today.year + 1)))

            newdep.folder = foldertmp
            newdep.slug = foldertmp
            newdep.create_date = timezone.now()
            newdep.save()
            Group.objects.get_or_create(name=f"{__package__.split('.')[1]}_{foldertmp}")
            return redirect(request.build_absolute_uri())
        else:
            messages.info(request, "Nama PPK atau Nama singkat sudah ada")

        form = DepartmentForm()
        context = {
            'data': data,
            'satkername': 'BALAI',
            'depurl': 'fm_balai_department',
            'form': form,
        }
        return render(request, 'file_manager/add_department.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class FolderListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        slug = request.GET.get("slug")
        year = request.GET.get("year")
        folder = request.GET.get("folder")

        folderlist = str(folder).split("/")
        if folderlist and folderlist[0] == '':
            folderlist.pop(0)

        path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder)
        contents = os.listdir(path)
        data = []

        for file in contents:
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                filemime, filesize, filetype, mime_type, mtime = get_fileinfo(full_path)
                icon_location = os.path.join('assets/filetypes', filemime)
                data.append({
                    'name': file,
                    'type': 'file',
                    'icon_location': icon_location,
                    'filesize': filesize,
                    'filetype': filetype,
                    'mimetype': mime_type,
                    'folder': folder,
                    'mtime': datetime.fromtimestamp(mtime),
                })
            else:
                mtime = os.path.getmtime(full_path)
                data.append({
                    'name': file,
                    'type': 'folder',
                    'link': os.path.join(folder, file),
                    'mtime': datetime.fromtimestamp(mtime),
                })

        context = {
            'data': data,
            'folder': folder,
            'showfolderurl': 'fm_balai_show_folder',
            'downloadurl': 'fm_balai_download',
            'slug': slug,
            'year': year,
            'zipfolderurl': 'fm_balai_download_folder',
            'renameurl': 'fm_balai_rename_file',
            'removeurl': 'fm_balai_remove_file',
        }
        return render(request, 'file_manager/folder_list.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class ShowFolderView(View):
    def get(self, request, slug, year):
        if not request.user.is_authenticated:
            return redirect('login')

        folder = request.GET.get("folder")
        dep = get_object_or_404(Department, slug=slug)

        context = {
            'slug': slug,
            'year': year,
            'depname': dep.name,
            'depslug': slug,
            'breadcrumbs': build_breadcrumbs(folder),
            'folder': folder,
            'satkername': 'BALAI',
            'depurl': 'fm_balai_department',
            'deplisturl': 'fm_balai_department_list',
            'folderlisturl': 'fm_balai_folder_list',
            'downloadurl': 'fm_balai_download',
            'depyearurl': 'fm_balai_department_year',
            'showfolderurl': 'fm_balai_show_folder',
            'addfolderurl': 'fm_balai_add_folder',
            'uploadfileurl': 'fm_balai_upload_file',
        }
        return render(request, 'file_manager/show_folder.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class AddFolderView(View):
    def get(self, request):
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
        form = AddFolderForm(initial={'year': year, 'slug': slug, 'folder': folder})
        return render(request, 'file_manager/add_folder.html', {'form': form})

    def post(self, request):
        foldername = request.POST.get('foldername')
        slug = request.POST.get("slug")
        year = str(request.POST.get("year"))
        folder = request.POST.get("folder")

        newfolder = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, foldername)
        if not os.path.exists(newfolder):
            os.mkdir(newfolder)
            message = f"penambahan folder {foldername} Sukses."
        else:
            message = f"penambahan folder {foldername} Gagal."

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": message
                })
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class UploadFileView(View):
    def get(self, request):
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
        return render(request, 'file_manager/upload_file.html', {
            'slug': slug,
            'year': year,
            'folder': folder
        })

    def post(self, request):
        if request.FILES:
            slug = request.POST.get("slug")
            year = str(request.POST.get("year"))
            folder = request.POST.get("folder")
            uploads = request.FILES.getlist('uploadfiles')
            for upload in uploads:
                pathlist = [__package__.split('.')[1], slug, year, str(folder).replace(os.path.sep, '$$'), str(upload)]
                filetmpname = "$$".join(pathlist)
                filetmppath = os.path.join(settings.MEDIA_ROOT, "tmpfiles", filetmpname)
                fss = FileSystemStorage()
                fss.save(filetmppath, upload)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "movieListChanged": None,
                        "showMessage": 'Upload File Sukses, tunggu beberapa saat kemudian refresh halaman'
                    })
                }
            )
        return HttpResponse(status=400)


@method_decorator(csrf_exempt, name='dispatch')
class RemoveFileView(View):
    def get(self, request):
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
        filename = request.GET.get("filename")
        type_ = request.GET.get("type")
        return render(request, 'file_manager/remove_file.html', {
            'slug': slug,
            'year': year,
            'folder': folder,
            'filename': filename,
            'type': type_
        })

    def post(self, request):
        filename = request.POST.get('filename')
        slug = request.POST.get("slug")
        year = str(request.POST.get("year"))
        folder = request.POST.get("folder")
        type_ = request.POST.get("type")

        path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, filename)
        if os.path.exists(path):
            if type_ == 'file':
                os.remove(path)
            else:
                shutil.rmtree(path)
            message = f"Hapus {type_} {filename} Sukses."
        else:
            message = f"Hapus {type_} {filename} Gagal."

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": message
                })
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class DownloadView(View):
    def get(self, request, slug, year):
        if not request.user.is_authenticated:
            return redirect('login')

        folder = request.GET.get("folder")
        filename = request.GET.get("filename")
        path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, filename)
        if os.path.exists(path):
            mime_type, encoding = mimetypes.guess_type(path)
            with open(path, 'rb') as file:
                response = HttpResponse(file.read(), content_type=mime_type)
                response['Content-Disposition'] = f'inline;filename={filename}'
                return response
        raise Http404


@method_decorator(csrf_exempt, name='dispatch')
class DownloadFolderView(View):
    def get(self, request):
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
        filename = request.GET.get("filename")
        return render(request, 'file_manager/download_folder.html', {
            'slug': slug,
            'year': year,
            'folder': folder,
            'filename': filename,
        })

    def post(self, request):
        slug = request.POST.get("slug")
        year = str(request.POST.get("year"))
        folder = request.POST.get("folder")
        filename = request.POST.get('filename')

        path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, filename)
        shutil.make_archive(path, "zip", path)
        message = "Zip File berhasil, tunggu beberapa saat apabila file zip belum ada"

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": message
                })
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class RenameFileView(View):
    def get(self, request):
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
        filename = request.GET.get("filename")
        form = RenameFileForm(initial={'newname': filename, 'year': year, 'slug': slug, 'folder': folder, 'filename': filename})
        return render(request, 'file_manager/rename_file.html', {'form': form})

    def post(self, request):
        newname = request.POST.get('newname')
        slug = request.POST.get("slug")
        year = str(request.POST.get("year"))
        folder = request.POST.get("folder")
        filename = request.POST.get("filename")

        existingfile = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, filename)
        newfile = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, newname)

        if os.path.exists(existingfile):
            os.rename(existingfile, newfile)
            message = f"perubahan nama {filename} Sukses."
        else:
            message = f"perubahan nama {filename} Gagal."

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": message
                })
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class Page404View(View):
    def get(self, request):
        return render(request, 'file_manager/page_404.html', {})
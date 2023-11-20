from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, Http404
from .models import Department
import sys
from django.template.defaultfilters import slugify
from .forms import DepartmentForm, AddFolderForm, RenameFileForm
import os, shutil
from django.conf import settings
from os.path import exists
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from sanitize_filename import sanitize
from django.contrib.auth.models import Group
from urllib.parse import unquote, urlparse
from django.contrib.auth.decorators import user_passes_test
from datetime import date, datetime
import mimetypes
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
import aioshutil
from asgiref.sync import sync_to_async

# tes commit
@csrf_exempt
def check_permission(request, depslug):
    if request.user.is_superuser:
        return True
    if depslug == '':
        groupname = __package__.split('.')[1]
    else: 
        groupname = __package__.split('.')[1] + "_" + depslug
    
    test_group1 = Group.objects.get(name=__package__.split('.')[1])
    test_group2 = Group.objects.get(name=groupname)
    user_group = request.user.groups.all()
    status1 = test_group1 in user_group
    status2 = test_group2 in user_group
    if status1:
        return status1
    else:
        return status2

@csrf_exempt
def department(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not check_permission(request, slug):
        return render(request=request, template_name='file_manager/page_404.html', context={'message':'Otorisasi Ditolak'})
        
    dep = Department.objects.filter(slug=slug)
    if not dep:
        return render(request=request, template_name='file_manager/page_404.html', context={'message':'Halaman tidak ada'})
    
    path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug)
    contents =os.listdir(path)    
    dep = Department.objects.filter(slug=slug).first()
    context = {
        "years": contents,
        'depname':dep.name,
        'slug': slug,
        'satkername': 'PJPA',
        'depurl': 'fm_pjpa_department',
        'deplisturl': 'fm_pjpa_department_list',
        'depyearurl': 'fm_pjpa_department_year',
        'showfolderurl': 'fm_pjpa_show_folder',
    }
    return render(request=request, template_name='file_manager/department2.html', context=context)

@csrf_exempt
def department_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    departments = Department.objects.all()
    data = []
    for dep in departments:
        data.append({
            'name': dep.name,
            'create_date': dep.create_date,
            'slug': dep.slug
        })
    
    context = {
        'data':data,
        'satkername': 'PJPA',
        'depurl': 'fm_pjpa_department',
    }

    return render(request=request, template_name='file_manager/department_list.html', context=context)
        

def checkfolder(path):
    contents =os.listdir(path)
    if len(contents) == 0:
        return False
    
    for file in contents:
        if os.path.isdir(os.path.join(path, file)):
            condirs = os.listdir(os.path.join(path, file))
            if len(condirs) != 0:
                return True
    return False

@csrf_exempt
def add_department(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not check_permission(request, ''):
        return render(request=request, template_name='file_manager/page_404.html', context={'message':'Otorisasi Ditolak'})
    departments = Department.objects.all()
    data = []
    for dep in departments:
        data.append({
            'name': dep.name,
            'create_date': dep.create_date,
            'slug': dep.slug
        })
    if request.method == 'POST':
        if request.POST.get('slug'):
            dep = Department.objects.get(slug=request.POST['slug'])
            if checkfolder(os.path.join(settings.FM_LOCATION, __package__.split('.')[1], dep.folder)):
                messages.info(request, "Tidak bisa dihapus karena ada folder terhubung")
                return redirect(request.build_absolute_uri())
            else:
                path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], dep.folder)
                dep.delete()
                shutil.rmtree(path)
                messages.info(request, "Hapus PPK Berhasil")
                return redirect(request.build_absolute_uri())
                
        form = DepartmentForm(request.POST)
        if form.is_valid():
            newdep = form.save(commit=False)
            foldertmp = slugify(newdep.shortname)
            if not exists(os.path.join(settings.FM_LOCATION, __package__.split('.')[1])):
                os.mkdir(os.path.join(settings.FM_LOCATION, __package__.split('.')[1]))
                          
            folder = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], foldertmp)
            if not exists(folder):
                os.mkdir(folder)
                today = date.today()
                os.mkdir(os.path.join(folder, str(today.year)))
                os.mkdir(os.path.join(folder, str(today.year+1)))
                
            newdep.folder = slugify(newdep.shortname)
            newdep.slug = slugify(newdep.shortname)
            

            newdep.create_date = timezone.now()
            newdep.save()
            Group.objects.get_or_create(name=f"{__package__.split('.')[1]}_{foldertmp}")
            return redirect(request.build_absolute_uri())
        else:
            messages.info(request, "Nama PPK atau Nama singkat sudah ada")    
    form = DepartmentForm()
    context = {
    'data':data,
    'satkername': 'PJPA',
    'depurl': 'fm_pjpa_department',
    'form':form,        
    }

    return render(request=request, template_name='file_manager/add_department.html', context=context)

def get_fileinfo(filepath):
    file_size = os.path.getsize(filepath)
    unit = 'bytes'
    if file_size < 90000000:
        unit = 'kb'
    elif file_size < 900000000:
        unit = 'mb'
    elif file_size < 9000000000:
        unit = 'gb'
    # print(file_size)    
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        file_size = round(size, 2)
    
    filesizestr = f"{str(file_size)} {unit}"    
    
    mime_type, encoding = mimetypes.guess_type(filepath)
    # print(mime_type)
    mtime = os.path.getmtime(filepath)
    if mime_type != None:
        if 'pdf' in mime_type:
            filemime, filetype = 'pdf.png', 'PDF'
        elif 'excel' in mime_type:
            filemime, filetype = 'excel.png', 'Excel'
        elif 'sheet' in mime_type:
            filemime, filetype = 'excel.png', 'Excel'
        elif 'png' in mime_type:
            filemime, filetype = 'image.png', 'Image'
        elif 'jpg' in mime_type:
            filemime, filetype = 'image.png', 'Image'
        elif 'jpeg' in mime_type:
            filemime, filetype = 'image.png', 'Image'
        elif 'mp3' in mime_type:
            filemime, filetype = 'sound.png', 'Image'
        elif 'video' in mime_type:
            filemime, filetype = 'video.png', 'Video'
        elif 'powerpoint' in mime_type:
            filemime, filetype = 'ppt.png', 'Power Point'
        elif  'presentation' in mime_type:
            filemime, filetype = 'ppt.png', 'Power Point'
        elif 'wordprocessingml' in mime_type:
            filemime, filetype = 'doc.png', 'Word'
        elif 'msword' in mime_type:
            filemime, filetype = 'doc.png', 'Word'
        elif 'compressed' in mime_type:
            filemime, filetype = 'zip.png', 'Zip'

        else:
            filemime, filetype = 'unknown.png', 'Unknown'
    else:
        filemime, filetype = 'unknown.png', 'Unknown'
                
    return filemime, filesizestr, filetype, mime_type, mtime

@csrf_exempt
def page_404(request):
    return render(request, 'file_manager/page_404.html', {})

def build_breadcrumbs(url):
    folderlist = str(url).split(os.path.sep )
    result = []
    for idx, folder in enumerate(folderlist):
        tmpl = []
        for i in range(0, idx+1):
            tmpl.append(folderlist[i])
        mdict = {
            'label': folder,
            'link': os.path.sep.join(tmpl),
        }
        result.append(mdict)
    result[-1]['link'] = ''
    return result

@csrf_exempt
def download(request, slug, year):
    if not request.user.is_authenticated:
        return redirect('login')
    folder = request.GET.get("folder")
    filename = request.GET.get("filename")
    path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, filename)
    # return HttpResponse(path)
    if exists(path):
        mime_type, encoding = mimetypes.guess_type(path)
        # return HttpResponse(mime_type)
        with open(path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type=f'{mime_type}')
            response['Content-Disposition'] = f'inline;filename={filename}'
            return response
    raise Http404

def folder_list(request):
    slug = request.GET.get("slug")
    year = request.GET.get("year")
    folder = request.GET.get("folder")
    
    folderlist = str(folder).split("/")
    folderlist.pop(0)
    path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder)
    contents =os.listdir(path)
    data = []
    for file in contents:
        if os.path.isfile(os.path.join(path, file)):
            filemime, filesize, filetype, mime_type, mtime = get_fileinfo(os.path.join(path, file))
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
            mtime = os.path.getmtime(os.path.join(path, file))
            data.append({
                'name': file,
                'type': 'folder',
                'link': os.path.join(folder, file),
                'mtime': datetime.fromtimestamp(mtime),
                
            })
    
    dep = Department.objects.get(slug=slug)        
    context = {
        'data': data,
        'folder': folder,
        'showfolderurl': 'fm_pjpa_show_folder',
        'downloadurl': 'fm_pjpa_download',
        'slug': slug,
        'year': year
}
    # return HttpResponse(context)
    return render(request=request, template_name='file_manager/folder_list.html', context=context)


def show_folder(request, slug, year):
    folder = request.GET.get("folder")
    dep = Department.objects.get(slug=slug)
    context = {
        'slug': slug,
        'year': year,
        'depname':dep.name,
        'depslug': slug,
        'breadcrumbs': build_breadcrumbs(folder),
        'folder': folder,
        'satkername': 'PJPA',
        'depurl': 'fm_pjpa_department',
        'deplisturl': 'fm_pjpa_department_list',
        'folderlisturl': 'fm_pjpa_folder_list',
        'downloadurl': 'fm_pjpa_download',
        'depyearurl': 'fm_pjpa_department_year',
        'showfolderurl': 'fm_pjpa_show_folder',
    }
    return render(request=request, template_name='file_manager/show_folder.html', context=context)

def add_folder(request):
    if request.method == "POST":
        foldername = request.POST.get('foldername')
        slug = request.POST.get("slug")
        year = str(request.POST.get("year"))
        folder = request.POST.get("folder")
        newfolder = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, foldername)
        if not exists(newfolder):
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
            })
    else:
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
        form = AddFolderForm(initial={'year': year, 'slug': slug, 'folder': folder})
    return render(request, 'file_manager/add_folder.html', {
        'form': form,
    })


def upload_file(request):
    if request.method == "POST":
        if request.FILES:
            slug = request.POST.get("slug")
            year = str(request.POST.get("year"))
            folder = request.POST.get("folder")
            uploads = request.FILES.getlist('uploadfiles')
            for upload in uploads:
                pathlist = [__package__.split('.')[1], slug, year, str(folder).replace(os.path.sep, '$$') ,str(upload)]
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
                })
    else:
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
    return render(request, 'file_manager/upload_file.html', {
        'slug': slug,
        'year': year,
        'folder': folder
    })

def remove_file(request):
    if request.method == "POST":
        filename = request.POST.get('filename')
        slug = request.POST.get("slug")
        year = str(request.POST.get("year"))
        folder = request.POST.get("folder")
        type = request.POST.get("type")

        path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, filename)
        if exists(path):
            if type=='file':
                os.remove(path)
            else:
                shutil.rmtree(path)
            message = f"Hapus { type } {filename} Sukses."
        else:
            message = f"Hapus { type } {filename} Gagal."
                    
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": message
                })
            })
    else:
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
        filename = request.GET.get("filename")
        type = request.GET.get("type")
        
    return render(request, 'file_manager/remove_file.html', {
        'slug': slug,
        'year': year,
        'folder': folder,
        'filename': filename,
        'type': type
    })

def zipfolder(path):
    return shutil.make_archive((path, "zip", path))
        
def download_folder(request):
    if request.method == "POST":
        filename = request.POST.get('filename')
        slug = request.POST.get("slug")
        year = str(request.POST.get("year"))
        folder = request.POST.get("folder")

        path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, filename)
        # await sync_to_async(zipfolder, thread_sensitive=True)
        shutil.make_archive(path, "zip", path)    
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": "Zip File berhasil, tunggu beberapa saat apabila file zip belum ada"
                })
            })
    else:
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

def rename_file(request):
    if request.method == "POST":
        newname = request.POST.get('newname')
        slug = request.POST.get("slug")
        year = str(request.POST.get("year"))
        folder = request.POST.get("folder")
        filename = request.POST.get("filename")
        existingfile = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, filename)
        newfile = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug, year, folder, newname)
        if exists(existingfile):
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
            })
    else:
        slug = request.GET.get("slug")
        year = str(request.GET.get("year"))
        folder = request.GET.get("folder")
        filename = request.GET.get("filename")
        form = RenameFileForm(initial={'newname':filename, 'year': year, 'slug': slug, 'folder': folder, 'filename': filename})
    return render(request, 'file_manager/rename_file.html', {
        'form': form,
    })

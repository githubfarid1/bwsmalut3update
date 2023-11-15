from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, Http404
from .models import Department, Subfolder, File
import sys
from django.template.defaultfilters import slugify
from .forms import FileForm, DepartmentForm, SubfolderForm
from taggit.models import Tag
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

def getmenu_year(department_id):
    years = Subfolder.objects.filter(department_id=department_id).order_by("year").values("year").distinct()
    yearlist = [int(x['year']) for x in years if x['year'] != '']
    today = date.today()
    if not today.year in yearlist:
        yearlist.append(today.year)
    if not today.year+1 in yearlist:    
        yearlist.append(today.year+1)
    yearlist.sort()
    return yearlist        

@csrf_exempt
def department(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not check_permission(request, slug):
        return render(request=request, template_name='fm_pjpa/page_404.html', context={'message':'Otorisasi Ditolak'})
        
    dep = Department.objects.filter(slug=slug)
    if not dep:
        return render(request=request, template_name='fm_pjpa/page_404.html', context={'message':'Halaman tidak ada'})
    
    # folder = request.GET.get("folder")
    path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], slug)
    contents =os.listdir(path)    
    # return HttpResponse(contents)
    dep = Department.objects.filter(slug=slug).first()
    context = {
        # 'data':subfolders,
        "years": contents,
        'depname':dep.name,
        'slug': slug,
    }
    return render(request=request, template_name='fm_pjpa/department.html', context=context)

@csrf_exempt
def department_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # if not check_permission(request, ''):
    #     return render(request=request, template_name='fm_pjpa/page_404.html', context={'message':'Otorisasi Ditolak'})
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
    }

    return render(request=request, template_name='fm_pjpa/department_list.html', context=context)
        
@csrf_exempt
def department_year(request, slug, year):
    if not request.user.is_authenticated:
        return redirect('login')
    if not check_permission(request, slug):
        return render(request=request, template_name='fm_pjpa/page_404.html', context={'message':'Otorisasi Ditolak'})
    dep = Department.objects.get(slug=slug)
    depfolder = dep.folder
    # subfolders = dep.subfolder_set.filter(year=year)
    # if request.method == 'POST':
    #     if request.POST.get('id'):
    #         subfolder = Subfolder.objects.get(id=request.POST['id'])
    #         if File.objects.filter(subfolder_id=subfolder.id).count() != 0:
    #             messages.info(request, "Tidak bisa dihapus karena ada file terhubung")
    #             return redirect(request.build_absolute_uri())
    #         else:
    #             path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], dep.folder, subfolder.year, subfolder.folder)
    #             # return HttpResponse(path)
    #             subfolder.delete()
    #             os.rmdir(path)
    #             messages.info(request, "Hapus Folder Berhasil")
    #             return redirect(request.build_absolute_uri())

    #     form = SubfolderForm(request.POST)
    #     if form.is_valid():
    #         newfloder = form.save(commit=False)
    #         foldertmp = slugify(newfloder.name)
    #         yeartmp = str(year)
    #         folder = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], depfolder, yeartmp)
    #         if not exists(folder):
    #             os.mkdir(folder)
    #         folder = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], depfolder, yeartmp, foldertmp)
    #         if exists(folder):
    #             messages.info(request, "Folder sudah ada")
    #             return redirect(request.build_absolute_uri())
    #         else:
    #             os.mkdir(folder)

    #         newfloder.folder = slugify(newfloder.name)
    #         newfloder.year = year
    #         newfloder.department_id = dep.id
    #         newfloder.create_date = timezone.now()
    #         newfloder.save()

    # form = SubfolderForm()
    # folder = request.GET.get("folder")
    data = []
    path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], depfolder, str(year))
    contents = os.listdir(path)    
    for file in contents:
        if os.path.isdir(os.path.join(path, file)):
            data.append(file)
    context = {
        'data': data,
        # "menu": getmenu_year(dep.id),
        'depname':dep.name,
        'slug': slug,
        'year': year,
        # 'form': form,
    }
    return render(request=request, template_name='fm_pjpa/department_year.html', context=context)

@csrf_exempt
def add_department(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not check_permission(request, ''):
        return render(request=request, template_name='fm_pjpa/page_404.html', context={'message':'Otorisasi Ditolak'})
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
            if Subfolder.objects.filter(department_id=dep.id).count() != 0:
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
    # 'depname':subfolder.department.name,
    # 'subfoldername': subfolder.name,
    # 'year': subfolder.year,
    # 'common_tags':common_tags,
    'form':form,        
    }

    return render(request=request, template_name='fm_pjpa/add_department.html', context=context)

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
def subfolder(request, id):
    # messages.info(request, "File Sudah ada")
    if not request.user.is_authenticated:
        return redirect('login')
    subfolder = Subfolder.objects.get(id=id)
    depslug = subfolder.department.slug
    if not check_permission(request, depslug):
        return render(request=request, template_name='fm_pjpa/page_404.html', context={'message':'Otorisasi Ditolak'})
    files = subfolder.file_set.all()
    data = []
    for file in files:
        filepath = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], file.subfolder.department.folder, str(file.subfolder.year), str(file.subfolder.folder), str(file.filename))
        filemime = 'unknown.png'
        filesize = 0
        filetype = 'Unknown'
        found = False
        mime_type = ''
        if exists(filepath):
            filemime, filesize, filetype, mime_type = get_fileinfo(filepath)
            # return HttpResponse(mime_type)
            found = True
            icon_location = os.path.join('assets/filetypes', filemime)
        else:
            icon_location = os.path.join('assets/filetypes', 'inprocess.png')
        data.append({'filename': file.filename,
                     'tags': file.tags,
                     'uuid_id': file.uuid_id,
                     'description': file.description,
                     'icon_location': icon_location,
                     'filesize': filesize,
                     'filetype': filetype,
                     'found': found,
                     'upload_date': file.upload_date,
                     })    
        
    common_tags = File.tags.most_common()[:10]
    if request.method == 'POST':
        if request.FILES and request.FILES['fileupload']:
            form = FileForm(request.POST)
            upload = request.FILES['fileupload']
            folderstrlist = [__package__.split('.')[1], subfolder.department.folder, str(subfolder.year), str(subfolder.folder)]
            folderstrlistwfile = folderstrlist.copy()
            folderstrlistwfile.append(str(upload))
            filetmpname = "$$".join(folderstrlistwfile)
            filetmppath = os.path.join(settings.MEDIA_ROOT, "tmpfiles", filetmpname)
            filepath = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], subfolder.department.folder, str(subfolder.year), str(subfolder.folder), str(upload))
            if exists(filepath) or exists(filetmppath):
                messages.info(request, "File Sudah ada")
                return redirect(request.build_absolute_uri())
            # print(form.errors)
            if form.is_valid():
                # breakpoint()
                newsubfolder = form.save(commit=False)
                newsubfolder.filename = upload
                slugs = "-".join([__package__.split('.')[1], subfolder.department.folder, str(subfolder.year), str(subfolder.folder), str(upload)])
                newsubfolder.slug = slugify(slugs)
                newsubfolder.subfolder_id = id
                newsubfolder.upload_date = timezone.now()
                newsubfolder.save()
                # Without this next line the tags won't be saved.
                form.save_m2m()
                fss = FileSystemStorage()
                fss.save(filetmppath, upload)
                # form = FileForm()
                return redirect(request.build_absolute_uri())
        else:
            doc = File.objects.get(uuid_id=request.POST['uuid_id'])
            doc.delete()
            subfolder = str(doc.subfolder.folder)
            year = str(doc.subfolder.year)
            depfolder = str(doc.subfolder.department.folder)
            filename = doc.filename
            path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], depfolder, year, subfolder, filename)
            folderstrlistwfile = [__package__.split('.')[1], depfolder, year, subfolder, filename]
            filetmpname = "$$".join(folderstrlistwfile)
            filetmppath = os.path.join(settings.MEDIA_ROOT, "tmpfiles", filetmpname)
            # print(filetmppath)
            if exists(filetmppath):
                os.remove(filetmppath)
            if exists(path):
                os.remove(path)
            
            return redirect(request.build_absolute_uri())

    else:
        form = FileForm()
    
    context = {
    'data':data,
    'depname':subfolder.department.name,
    'subfoldername': subfolder.name,
    'year': subfolder.year,
    'common_tags':common_tags,
    'form':form,
    'depslug': depslug      
    }

    return render(request=request, template_name='fm_pjpa/subfolder.html', context=context)

@csrf_exempt
def filedownload(request, uuid_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    doc = File.objects.get(uuid_id=uuid_id)
    subfolder = str(doc.subfolder.folder)
    year = str(doc.subfolder.year)
    depfolder = str(doc.subfolder.department.folder)
    filename = doc.filename
    path = os.path.join(settings.FM_LOCATION, __package__.split('.')[1], depfolder, year, subfolder, filename)
    # return HttpResponse(path)
    if exists(path):
       
        mime_type, encoding = mimetypes.guess_type(path)
        # return HttpResponse(mime_type)
        with open(path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type=f'{mime_type}')
            response['Content-Disposition'] = f'inline;filename={filename}'
            return response
    raise Http404

@csrf_exempt
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    files = File.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'data':files,
    }
    return render(request, 'fm_pjpa/subfolder.html', context)

@csrf_exempt
def page_404(request):
    return render(request, 'fm_pjpa/page_404.html', {})

def build_breadcrumbs(url):
    folderlist = str(url).split("/")
    result = []
    maxcount = len(folderlist)
    for idx, folder in enumerate(folderlist):
        tmpl = []
        for i in range(0, idx+1):
            tmpl.append(folderlist[i])
        mdict = {
            'label': folder,
            'link': '/'.join(tmpl),
        }
        result.append(mdict)
    result[-1]['link'] = ''
    return result

def showfolder(request, slug, year):
    folder = request.GET.get("folder")
    folderlist = str(folder).split("/")
    curfolder = folderlist[0]
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
        'slug': slug,
        'year': year,
        'depname':dep.name,
        'depslug': slug,
        'breadcrumbs': build_breadcrumbs(folder),
        'folder': folder,
        # 'folderlist': folderlist
    }
    return render(request=request, template_name='fm_pjpa/showfolder.html', context=context)

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

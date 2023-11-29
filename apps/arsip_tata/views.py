from django.shortcuts import render
import os
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, Http404
from .models import Year, Box, Bundle, Item, Customer, Trans, TransDetail
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import YearForm, BoxForm, BundleForm, ItemForm, CustomerForm, TransForm, AddTransDetailForm, EditTransDetailForm, SearchItemForm
from django.views.decorators.http import require_POST
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.styles.borders import Border, Side

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageTemplate, BaseDocTemplate, Frame, Spacer
from reportlab.lib.units import inch
from reportlab.platypus.tables import Table,TableStyle,colors
from datetime import datetime, timedelta
from django.template.defaultfilters import slugify
from django.db.models import Q


# Create your views here.
@csrf_exempt
def year_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'arsip_tata/year_list.html', {
        'years': Year.objects.all(),
    })
    
def show_year(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='arsip_tata/show_year.html', context=context)
    
def add_year(request):
    if request.method == "POST":
        form = YearForm(request.POST)
        if form.is_valid():
            year = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "yearListChanged": None,
                        "showMessage": f"{year.yeardate} added."
                    })
                })
    else:
        form = YearForm()
    return render(request, 'arsip_tata/year_form.html', {
        'form': form,
        'module': 'Tambah Data'
    })


def edit_year(request, pk):
    year = get_object_or_404(Year, pk=pk)
    # return HttpResponse(year.id)
    if request.method == "POST":
        form = YearForm(request.POST, instance=year)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "yearListChanged": None,
                        "showMessage": f"{year.yeardate} updated."
                    })
                }
            )
    else:
        form = YearForm(instance=year)
    return render(request, 'arsip_tata/year_form.html', {
        'form': form,
        'year': year,
        'module': 'Edit Data'
    })

@ require_POST
def remove_year(request, pk):
    year = get_object_or_404(Year, pk=pk)
    year.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "yearListChanged": None,
                "showMessage": f"{year.yeardate} deleted."
            })
        })


def show_boxes(request, year):
    if not request.user.is_authenticated:
        return redirect('login')
    year = Year.objects.get(yeardate=year)
    context = {
        'year_id': year.id,
        'year_date': year.yeardate
    }
    return render(request=request, template_name='arsip_tata/show_box.html', context=context)

@csrf_exempt
def box_list(request, year_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    boxes = Box.objects.filter(year_id=year_id)
    return render(request, 'arsip_tata/box_list.html', {
        'boxes': boxes,
    })

def add_box(request, year_id):
    if request.method == "POST":
        form = BoxForm(request.POST)
        if form.is_valid():
            box = form.save(commit=False)
            year = Year.objects.get(id=year_id)
            box.year_id = year_id
            box.yeardate = year.yeardate
            box.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "boxListChanged": None,
                        "showMessage": f"{box.box_number} added."
                    })
                })
    else:
        year = Year.objects.get(id=year_id)
        form = BoxForm(initial={'yeardate': year.yeardate})
    return render(request, 'arsip_tata/box_form.html', {
        'form': form,
    })

def edit_box(request, pk):
    box = get_object_or_404(Box, pk=pk)
    if request.method == "POST":
        form = BoxForm(request.POST, instance=box)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "boxListChanged": None,
                        "showMessage": f"{box.box_number} updated."
                    })
                }
            )
    else:
        form = BoxForm(instance=box)
    return render(request, 'arsip_tata/box_form.html', {
        'form': form,
        'box': box,
        'module': 'Edit Data'
    })

@ require_POST
def remove_box(request, pk):
    box = get_object_or_404(Box, pk=pk)
    box.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "boxListChanged": None,
                "showMessage": f"{box.box_number} deleted."
            })
        })

def show_bundles(request, year_date, box_number):
    if not request.user.is_authenticated:
        return redirect('login')
    year = Year.objects.get(yeardate=year_date)
    box = Box.objects.filter(year_id=year.id, box_number=box_number).first()
    
    context = {
        'box_id': box.id,
        'box_number': box_number,
        'year_date': year_date
    }
    return render(request=request, template_name='arsip_tata/show_bundle.html', context=context)

@csrf_exempt
def bundle_list(request, box_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    bundles = Bundle.objects.filter(box_id=box_id)
    return render(request, 'arsip_tata/bundle_list.html', {
        'bundles': bundles,
    })

def add_bundle(request, box_id):
    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            bundle = form.save(commit=False)
            bundle.box_id = box_id
            # bundle.code = bundle.bundlecode.name.split(" - ")[0]
            # box = Box.objects.get(id=box_id)
            # bundle.yeardate = box.yeardate
            bundle.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "bundleListChanged": None,
                        "showMessage": f"{bundle.bundle_number} added."
                    })
                })
    else:
        box = Box.objects.get(id=box_id)
        form = BundleForm(initial={'yeardate': box.yeardate})
    return render(request, 'arsip_tata/bundle_form.html', {
        'form': form,
    })

def edit_bundle(request, pk):
    bundle = get_object_or_404(Bundle, pk=pk)
    if request.method == "POST":
        form = BundleForm(request.POST, instance=bundle)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "bundleListChanged": None,
                        "showMessage": f"{bundle.bundle_number} updated."
                    })
                }
            )
    else:
        form = BundleForm(instance=bundle)
    return render(request, 'arsip_tata/bundle_form.html', {
        'form': form,
        'bundle': bundle,
        'module': 'Edit Data'
    })

@ require_POST
def remove_bundle(request, pk):
    bundle = get_object_or_404(Bundle, pk=pk)
    bundle.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "bundleListChanged": None,
                "showMessage": f"{bundle.bundle_number} deleted."
            })
        })

def show_items(request, year_date, bundle_number):
    if not request.user.is_authenticated:
        return redirect('login')
    bundle = Bundle.objects.filter(yeardate=year_date, bundle_number=bundle_number).first()
    context = {
        'bundle': bundle,
        'year_date': year_date
    }
    return render(request=request, template_name='arsip_tata/show_item.html', context=context)

@csrf_exempt
def item_list(request, bundle_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    items = Item.objects.filter(bundle_id=bundle_id).order_by('item_number')
    return render(request, 'arsip_tata/item_list.html', {
        'items': items,
    })

def add_item(request, bundle_id):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.bundle_id = bundle_id
            item.total = item.copy + item.original
            bundle = Bundle.objects.get(id=bundle_id)
            item.codegen = "-".join([str(item.yeardate), str(bundle.box.box_number), str(bundle.bundle_number), str(item.item_number)])
            item.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "itemListChanged": None,
                        "showMessage": f"{item.item_number} added."
                    })
                })
    else:
        bundle = Bundle.objects.get(id=bundle_id)
        form = ItemForm(initial={'yeardate': bundle.yeardate})
    return render(request, 'arsip_tata/item_form.html', {
        'form': form,
    })

def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            itemsave = form.save(commit=False)
            itemsave.total = itemsave.copy + itemsave.original
            # bundle = Bundle.objects.get(id=item.bundle_id)
            itemsave.codegen = "-".join([str(itemsave.yeardate), str(item.bundle.box.box_number), str(item.bundle.bundle_number), str(itemsave.item_number)])
            itemsave.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "itemListChanged": None,
                        "showMessage": f"{itemsave.item_number} updated."
                    })
                }
            )
    else:
        form = ItemForm(instance=item)
    return render(request, 'arsip_tata/item_form.html', {
        'form': form,
        'item': item,
        'module': 'Edit Data'
    })

@ require_POST
def remove_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "itemListChanged": None,
                "showMessage": f"{item.item_number} deleted."
            })
        })

def create_xls(datalist, sheet, year):
    # wb = Workbook()
    # sheet = wb.active
    sheet.title = str(year)
    sheet.column_dimensions['A'].width = 7
    sheet.column_dimensions['B'].width = 7
    sheet.column_dimensions['C'].width = 8
    sheet.column_dimensions['D'].width = 20
    sheet.column_dimensions['E'].width = 60
    sheet.column_dimensions['F'].width = 7
    sheet.column_dimensions['G'].width = 2
    sheet.column_dimensions['H'].width = 6 
    sheet.column_dimensions['I'].width = 7 
    sheet.column_dimensions['J'].width = 7
    sheet.column_dimensions['K'].width = 7
    sheet.column_dimensions['L'].width = 30

    sheet.merge_cells('A1:L1')
    sheet.merge_cells('A2:L2')
    sheet.merge_cells('A3:L3')
    aligncenter = Alignment(horizontal='center')
    headerfont = Font(name='Arial Narrow', size=14, bold=True)
    sheet['A1'] = "DAFTAR ARSIP INAKTIF"
    sheet['A1'].alignment = aligncenter
    sheet['A1'].font = headerfont
    sheet['A2'] = "UNIT PENGOLAH: BALAI WILAYAH SUNGAI MALUKU UTARA"
    sheet['A2'].alignment = aligncenter
    sheet['A2'].font = headerfont
    sheet['A3'] = "TAHUN PENATAAN {}".format(year)
    sheet['A3'].alignment = aligncenter
    sheet['A3'].font = headerfont
    
    centervh = Alignment(horizontal='center', vertical='center', wrap_text=True)
    centerv = Alignment(vertical='center', wrap_text=True)
    wraptxt = Alignment(wrap_text=True)

    thin_border1 = Border(left=Side(style='thin'), 
                        right=Side(style='thin'), 
                        top=Side(style='thin'), 
                        bottom=Side(style='thin'))
    
    thin_border2 = Border(bottom=Side(style='thin'),right=Side(style='thin'),left=Side(style='thin'))
    thin_border3 = Border(top=Side(style='thin'), right=Side(style='thin'),left=Side(style='thin'))
    thin_border4 = Border(right=Side(style='thin'),left=Side(style='thin'))
    thin_border5 = Border(top=Side(style='thin'), bottom=Side(style='thin'))
    thin_border6 = Border(top=Side(style='thin'))
    thin_border7 = Border(bottom=Side(style='thin'))
    thin_border8 = Border(left=Side(style='thin'))
    thin_border9 = Border(right=Side(style='thin'))


    font_style1 = Font(name='Arial Narrow', size=11, bold=True)
    font_style2 = Font(name='Arial', size=8.5)
    font_style3 = Font(name='Arial', size=8.5, italic=True)
    color1 = PatternFill(start_color="c6d5f7", fill_type = "solid")

    # sheet.row_dimensions[7].height = 28
    for cell in sheet["7:7"]:
        cell.alignment = centervh
        cell.font = font_style1
    for cell in sheet["8:8"]:
        cell.alignment = centervh
        cell.font = font_style1

    sheet.merge_cells('A7:A8')
    sheet.merge_cells('B7:B8')
    sheet.merge_cells('C7:C8')
    sheet.merge_cells('D7:D8')
    sheet.merge_cells('E7:E8')
    sheet.merge_cells('F7:F8')
    sheet.merge_cells('G7:H8')
    sheet.merge_cells('I7:K7')
    sheet.merge_cells('L7:L8')
    sheet.merge_cells('I8:J8')
    sheet.merge_cells('G9:H9')
    sheet.merge_cells('I9:J9')

    
    headers = ("NO BRKS", "NO URUT", "KODE", "INDEKS/JUDUL", "URAIAN MASALAH / KEGIATAN", "TAHUN")
    for i in headers:
        sheet.cell(row=7, column=headers.index(i)+1).value = i
        sheet.cell(row=7, column=headers.index(i)+1).border = thin_border1
        sheet.cell(row=8, column=headers.index(i)+1).border = thin_border1
    no = 0
    for i in range(1, 13):
        if i not in [8,10]:
            no += 1
            sheet.cell(row=9, column=i).value = no
            
        sheet.cell(row=9, column=i).alignment = centervh
        sheet.cell(row=9, column=i).border = thin_border1
        sheet.cell(row=9, column=i).font = Font(name='Arial Narrow', size=8, bold=True)
        sheet.cell(row=7, column=i).fill = color1
        sheet.cell(row=8, column=i).fill = color1
        sheet.cell(row=9, column=i).fill = color1

    sheet.row_dimensions[9].height = 9
    
    sheet.cell(row=7, column=7).value = "JUMLAH BERKAS"
    sheet.cell(row=7, column=7).border = thin_border1
    sheet.cell(row=8, column=7).border = thin_border1
    sheet.cell(row=7, column=8).border = thin_border1
    sheet.cell(row=8, column=8).border = thin_border1

    sheet.cell(row=7, column=9).value = "KETERANGAN"
    sheet.cell(row=7, column=9).border = thin_border1
    sheet.cell(row=7, column=10).border = thin_border1
    sheet.cell(row=7, column=11).border = thin_border1


    sheet.cell(row=8, column=9).value = "ASLI/COPY"
    sheet.cell(row=8, column=9).border = thin_border1
    sheet.cell(row=8, column=10).border = thin_border1
    
    sheet.cell(row=8, column=11).value = "BOX"
    
    sheet.cell(row=8, column=9).border = thin_border1

    sheet.cell(row=8, column=10).border = thin_border1
    sheet.cell(row=8, column=11).border = thin_border1
    
    
    sheet.cell(row=8, column=9).font = font_style1
    sheet.cell(row=8, column=10).font = font_style1
    sheet.cell(row=8, column=11).font = font_style1
    sheet.cell(row=8, column=12).font = font_style1
    
    sheet.cell(row=7, column=12).value = "KLASIFIKASI KEAMANAN DAN AKSES ARSIP DINAMIS"
    sheet.cell(row=7, column=12).border = thin_border1
    sheet.cell(row=8, column=12).border = thin_border1
    sheet.cell(row=7, column=12).alignment = centervh

    i = 10
    for res in datalist:
        sheet['{}{}'.format('K', i)].border = thin_border4
        sheet['{}{}'.format('A', i)].border = thin_border4
        sheet['{}{}'.format('B', i)].border = thin_border4
        sheet['{}{}'.format('C', i)].border = thin_border4
        sheet['{}{}'.format('D', i)].border = thin_border4
        sheet['{}{}'.format('E', i)].border = thin_border4
        sheet['{}{}'.format('F', i)].border = thin_border4
        sheet['{}{}'.format('G', i)].border = thin_border7
        sheet['{}{}'.format('H', i)].border = thin_border7
        sheet['{}{}'.format('I', i)].border = thin_border4
        sheet['{}{}'.format('J', i)].border = thin_border4
        sheet['{}{}'.format('L', i)].border = thin_border4

        sheet['{}{}'.format('B', i)].border = thin_border1
        sheet['{}{}'.format('E', i)].border = thin_border1
        # sheet['{}{}'.format('G', i)].border = thin_border7
        # sheet['{}{}'.format('H', i)].border = thin_border1
        sheet['{}{}'.format('I', i)].border = thin_border1
        sheet['{}{}'.format('J', i)].border = thin_border1
        sheet['{}{}'.format('L', i)].border = thin_border1
            
        sheet['{}{}'.format('A', i)].value = res[0]
        sheet['{}{}'.format('B', i)].value = res[1]
        sheet['{}{}'.format('C', i)].value = res[2]
        sheet['{}{}'.format('D', i)].value = res[3]
        sheet['{}{}'.format('E', i)].value = res[4]
        sheet['{}{}'.format('F', i)].value = res[5]
        sheet['{}{}'.format('H', i)].value = res[6]
        sheet['{}{}'.format('I', i)].value = res[7]
        sheet['{}{}'.format('J', i)].value = res[8]
        sheet['{}{}'.format('K', i)].value = res[9]
        sheet['{}{}'.format('L', i)].value = res[10]
        sheet['{}{}'.format('K', i)].alignment = centervh
        sheet['{}{}'.format('A', i)].alignment = centervh
        sheet['{}{}'.format('B', i)].alignment = centervh
        sheet['{}{}'.format('C', i)].alignment = centervh
        sheet['{}{}'.format('D', i)].alignment = centervh
        sheet['{}{}'.format('E', i)].alignment = centerv
        sheet['{}{}'.format('F', i)].alignment = centervh
        # sheet['{}{}'.format('G', i)].alignment = centervh
        sheet['{}{}'.format('H', i)].alignment = centervh
        sheet['{}{}'.format('I', i)].alignment = centervh
        sheet['{}{}'.format('J', i)].alignment = centervh
        sheet['{}{}'.format('L', i)].alignment = centervh
        if res[0] != '':
            sheet['{}{}'.format('A', i)].border = thin_border3
            sheet['{}{}'.format('C', i)].border = thin_border3
            sheet['{}{}'.format('D', i)].border = thin_border3
            sheet['{}{}'.format('F', i)].border = thin_border3
        if res[9] != '':
            sheet['{}{}'.format('K', i)].border = thin_border3

        i += 1

    sheet['{}{}'.format('A', i)].border = thin_border6
    sheet['{}{}'.format('C', i)].border = thin_border6
    sheet['{}{}'.format('D', i)].border = thin_border6
    sheet['{}{}'.format('F', i)].border = thin_border6
    sheet['{}{}'.format('K', i)].border = thin_border6

def generate_data(year):
    result = []
    yeardata = Year.objects.get(yeardate=year)
    for box in yeardata.box_set.all():
        cbox = True
        for bundle in box.bundle_set.all():
            cbundle = True
            for item in bundle.item_set.all().order_by('item_number'):
                if cbox:
                    boxnumber = box.box_number
                    cbox = False
                else:
                    boxnumber = ''

                if cbundle:
                    bundlenumber = bundle.bundle_number
                    code = bundle.code
                    creator = bundle.creator
                    description = f"{item.title}\n{bundle.description}"
                    year_bundle = bundle.year_bundle
                    cbundle = False
                else:
                    bundlenumber = ''
                    code = ''
                    creator = ''
                    description = item.title
                    year_bundle = ''
                
                dataset = (bundlenumber, item.item_number, code, creator, description, year_bundle, item.total, item.original, item.copy, boxnumber, item.get_accesstype_display())
                result.append(dataset)
    return result

def report(request, year):
    res = generate_data(year)
    wb = Workbook()
    filename = f"data_{__package__.split('.')[1]}_tahun_penataan_{year}.xlsx"
    sheet = wb.active
    create_xls(datalist=res, sheet=sheet, year=year)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)    
    wb.save(response)
    return response

def show_customers(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='arsip_tata/show_customer.html', context=context)

def customer_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'arsip_tata/customer_list.html', {
        'customers': Customer.objects.all(),
    })

def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "customerListChanged": None,
                        "showMessage": f"{customer.name} added."
                    })
                })
    else:
        form = CustomerForm()
    return render(request, 'arsip_tata/customer_form.html', {
        'form': form,
        'module': 'Tambah Data'
    })

def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "customerListChanged": None,
                        "showMessage": f"{customer.name} updated."
                    })
                }
            )
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'arsip_tata/customer_form.html', {
        'form': form,
        'customer': customer,
        'module': 'Edit Data'
    })

@ require_POST
def remove_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "customerListChanged": None,
                "showMessage": f"{customer.name} deleted."
            })
        })


def show_trans(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='arsip_tata/show_trans.html', context=context)

def trans_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'arsip_tata/trans_list.html', {
        'trans': Trans.objects.all().order_by("-id"),
    })

def add_trans(request):
    if request.method == "POST":
        form = TransForm(request.POST)
        if form.is_valid():
            trans = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "transListChanged": None,
                        "showMessage": f"{trans.id} added."
                    })
                })
    else:
        form = TransForm()
    return render(request, 'arsip_tata/trans_form.html', {
        'form': form,
        'module': 'Tambah Data'
    })

def edit_trans(request, pk):
    trans = get_object_or_404(Trans, pk=pk)
    if request.method == "POST":
        form = TransForm(request.POST, instance=trans)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "transListChanged": None,
                        "showMessage": f"{trans.id} updated."
                    })
                }
            )
    else:
        form = TransForm(instance=trans)
    return render(request, 'arsip_tata/trans_form.html', {
        'form': form,
        'trans': trans,
        'module': 'Edit Data'
    })

@ require_POST
def remove_trans(request, pk):
    trans = get_object_or_404(Trans, pk=pk)
    trans.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "transListChanged": None,
                "showMessage": f"{trans.id} deleted."
            })
        })

def show_trans_detail(request, trans_id):
    if not request.user.is_authenticated:
        return redirect('login')
    trans = Trans.objects.get(id=trans_id)
    context = {
        'trans': trans,
    }
    return render(request=request, template_name='arsip_tata/show_trans_detail.html', context=context)

@csrf_exempt
def trans_detail_list(request, trans_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    transdetail = TransDetail.objects.filter(trans_id=trans_id)
    return render(request, 'arsip_tata/trans_detail_list.html', {
        'transdetail': transdetail,
    })

@csrf_exempt
def add_trans_detail(request, trans_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        code = request.POST.get('code')
        # form = AddTransDetailForm(request.POST)
        try:
            # year, box, bundle, item = code.split("-")
            message = f"Kode item berkas {code} sukses"
            item = Item.objects.get(codegen=code)
            if item:
                if item.total == 1:
                    message = f"Kode item berkas {code} hanya ada 1, tidak boleh pinjam lebih dari 1 hari"
                
                td = TransDetail.objects.filter(item_id=item.id, date_return__isnull=True)
                if td.count() != 0:
                    message = f"Kode item berkas {code} sedang dipinjam"
                else:
                    td = TransDetail(item_id=item.id, trans_id=trans_id)
                    td.save()
                    message = f"Kode item berkas {code} tersimpan"
        except:
            message = f"Kode item berkas {code} tidak ada"
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "transDetailListChanged": None,
                    "showMessage": message
                })
            })
    else:
        form = AddTransDetailForm()
    return render(request, 'arsip_tata/add_trans_detail_form.html', {
        'form': form,
        'module': 'Tambah Data'
    })

# @ require_POST
def remove_transdetail(request, pk):
    if request.method == "POST":
        trans = get_object_or_404(TransDetail, pk=pk)
        trans_id = trans.trans.id
        trans.delete()
        return redirect('arsip_tata_show_trans_detail', trans_id=trans_id)

def trans_form(request, pk):
    trans = Trans.objects.get(pk=pk)
    detail = trans.transdetail_set.all()
    pdf = io.BytesIO()
    doc = SimpleDocTemplate(pdf, pagesize=A4)
    date1 = trans.date_trans
    date1show = date1.strftime('%d %B %Y')
    date2 = date1 + timedelta(days=7)
    date2show = date2.strftime('%d %B %Y')
    styles = getSampleStyleSheet()
    title = "Form Peminjaman Dokumen"

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
    template = PageTemplate(frames=[frame], id='mytemplate')

    doc.addPageTemplates([template])
    elements = []
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f'Nama Peminjam: <strong>{trans.customer.name}</strong>', styles['Normal']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f'No WhatsApp: <strong>{trans.customer.phone_number}</strong>', styles['Normal']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f'Tanggal Pinjam: <strong>{date1show}</strong>', styles['Normal']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f'Akan Kembali pada: <strong>{date2show}</strong>', styles['Normal']))
    mydata = []
    mydata.append(("No", "Kode", "Judul Dokumen"))
    c_width = [0.4*inch, 1*inch, 5*inch]
    
    style2 = getSampleStyleSheet()
    style2 = style2["BodyText"]
    style2.wordWrap = 'CJK'
    filename = f"form_pinjam_{slugify(trans.customer.name)}.pdf"
    for idx, data in enumerate(detail):
        myset = (Paragraph(str(idx+1), style2) , Paragraph(data.item.codegen, style2), Paragraph(data.item.title + "<br/>" + data.item.bundle.description.replace("\n", "<br/>") , style2))
        mydata.append(myset)
    
    mytable = Table(mydata, colWidths=c_width, hAlign='LEFT')
    mytable.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgreen),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.red),
                       ('FONTSIZE',(0,0),(-1,0),12),
                       ('FONTSIZE',(0,1),(-1,-1),8),
                       ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
                       ('ALIGN', (0,0), (-1,0), 'CENTER'),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('VALIGN',(0,0),(-1,-1),'TOP'),
                       ]))
    elements.append(Spacer(1, 10))
    elements.append(mytable)

    doc.build(elements)
    pdf.seek(0)
    response = HttpResponse(pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline;filename={filename}'
    return response

def show_transret(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='arsip_tata/show_transret.html', context=context)

def transret_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'arsip_tata/transret_list.html', {
        'trans': Trans.objects.all().order_by("-id"),
    })

def show_transret_detail(request, trans_id):
    if not request.user.is_authenticated:
        return redirect('login')
    trans = Trans.objects.get(id=trans_id)
    context = {
        'trans': trans,
    }
    return render(request=request, template_name='arsip_tata/show_transret_detail.html', context=context)

def edit_transdetail(request, pk):
    trans = get_object_or_404(TransDetail, pk=pk)
    if request.method == "POST":
        form = EditTransDetailForm(request.POST, instance=trans)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "transretDetailListChanged": None,
                        "showMessage": f"{trans.id} updated."
                    })
                }
            )
    else:
        if trans.date_return == None:
            form = EditTransDetailForm(instance=trans)
        else:
            trans.date_return = None
            trans.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "transretDetailListChanged": None,
                        "showMessage": f"{trans.id} updated."
                    })
                }
            )

    return render(request, 'arsip_tata/edit_trans_detail_form.html', {
        'form': form,
        'transdetail': trans,
        'module': 'Edit Data'
    })

@csrf_exempt
def transret_detail_list(request, trans_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    transdetail = TransDetail.objects.filter(trans_id=trans_id)
    return render(request, 'arsip_tata/transret_detail_list.html', {
        'transdetail': transdetail,
    })

def transret_form(request, pk):
    trans = Trans.objects.get(pk=pk)
    detail = trans.transdetail_set.all()
    pdf = io.BytesIO()
    doc = SimpleDocTemplate(pdf, pagesize=A4)
    date1 = trans.date_trans
    date1show = date1.strftime('%d %B %Y')
    styles = getSampleStyleSheet()
    title = "Form Pengembalian Dokumen"

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
    template = PageTemplate(frames=[frame], id='mytemplate')

    doc.addPageTemplates([template])
    elements = []
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f'Nama Peminjam: <strong>{trans.customer.name}</strong>', styles['Normal']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f'No WhatsApp: <strong>{trans.customer.phone_number}</strong>', styles['Normal']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f'Tanggal Pinjam: <strong>{date1show}</strong>', styles['Normal']))
    elements.append(Spacer(1, 6))
    mydata = []
    mydata.append(("No", "Kode", "Judul Dokumen", "Kembali"))
    c_width = [0.4*inch, 1*inch, 4*inch, 1*inch]
    
    style2 = getSampleStyleSheet()
    style2 = style2["BodyText"]
    style2.wordWrap = 'CJK'
    filename = f"form_kembali_{slugify(trans.customer.name)}.pdf"
    for idx, data in enumerate(detail):
        if data.date_return:
            date_return = data.date_return.strftime('%d %b %Y')
        else:
            date_return = ""
        myset = (Paragraph(str(idx+1), style2) , Paragraph(data.item.codegen, style2), Paragraph(data.item.title + "<br/>" + data.item.bundle.description.replace("\n", "<br/>") , style2), Paragraph(date_return, style2))
        mydata.append(myset)

    mytable = Table(mydata, colWidths=c_width, hAlign='LEFT')
    mytable.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightblue),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.red),
                       ('FONTSIZE',(0,0),(-1,0),12),
                       ('FONTSIZE',(0,1),(-1,-1),8),
                       ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
                       ('ALIGN', (0,0), (-1,0), 'CENTER'),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('VALIGN',(0,0),(-1,-1),'TOP'),
                       ]))
    elements.append(Spacer(1, 10))
    elements.append(mytable)

    doc.build(elements)
    pdf.seek(0)
    response = HttpResponse(pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline;filename={filename}'
    return response

def search_item(request):
    context = {}
    if request.GET.get("title") or request.GET.get("description"):
        title = request.GET.get("title")
        description = request.GET.get("description")
        if title != None and description == None:
            items = Item.objects.filter(title__icontains=title)
        elif title == None and description != None:
            items = Item.objects.filter(bundle__description__icontains=description)
        else:
            items = Item.objects.filter(Q(bundle__description__icontains=description) & Q(title__icontains=title))       
        data = []
        for item in items:
            status = 'Ada'
            trans_id = None
            if item.transdetail_set.filter(date_return__isnull=True).count() != 0:
                status='Dipinjam'
                trans_id = item.transdetail_set.filter(date_return__isnull=True).first().trans_id
            myset = (item.codegen, item.title, item.bundle.description, status, trans_id)
            data.append(myset)
        context['data'] = data
    
    context['form'] = SearchItemForm()
    return render(request,'arsip_tata/search_item_form.html', context=context)

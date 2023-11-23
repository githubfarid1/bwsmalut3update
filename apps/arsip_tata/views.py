from django.shortcuts import render
import os
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, Http404
from .models import Year, Box, Bundle, Item
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import YearForm, BoxForm, BundleForm, ItemForm
from django.views.decorators.http import require_POST


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
        form = BoxForm()
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
            box = Box.objects.get(id=box_id)
            bundle.yeardate = box.yeardate
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
        form = BundleForm()
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
            item.yeardate = bundle.yeardate
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
        form = ItemForm()
    return render(request, 'arsip_tata/item_form.html', {
        'form': form,
    })

def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.total = item.copy + item.original
            item.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "itemListChanged": None,
                        "showMessage": f"{item.item_number} updated."
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

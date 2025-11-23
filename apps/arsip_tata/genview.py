
from .models import Year, Box, Bundle, Item, Customer, Trans, TransDetail, Package, PackageItem
from django.conf import settings
import os
from django.db.models import Q, Max, Count, Sum

class GenerateScriptView:
    def __init__(self, request, form, template_name) -> None:
        # self.__year = year
        self.__request = request
        self.__form = form
        self.__template_name = template_name
        
    def gencontext(self):
        if self.__request.GET.get("search"):
            query = self.__request.GET.get("search")
            items = Item.objects.filter(Q(title__icontains=query)  | Q(bundle__description__icontains=query))
        else:
            items = Item.objects.all().order_by("-uploaded_date")[:50]
        datalist = []
        for ke, item in enumerate(items):
            folder = str(item.bundle.yeardate)
            # breakpoint()
            path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], folder, "-".join([str(item.bundle.yeardate), str(item.bundle.box.box_number), str(item.bundle.bundle_number), str(item.item_number)]) + ".pdf")
            pdffound = False
            if os.path.exists(path):
                pdffound = True
            if item.cover:
                coverurl = item.cover.url
            else:
                coverurl = ""
            datalist.append({
                "box_number": item.bundle.box.box_number,
                "bundle_number": item.bundle.bundle_number,
                "doc_number": item.item_number,
                "bundle_code": item.bundle.code,
                "bundle_title": item.bundle.description,
                "bundle_year": item.bundle.year_bundle,
                "doc_description": item.title,
                "doc_count": item.total,
                "bundle_orinot": "", #item.bundle.orinot,
                "row_number": ke + 1,
                "pdffound": pdffound,
                "doc_id": item.id,
                "coverfilepath": coverurl,
                "filesize": item.filesize,
                "pagecount": item.page_count,
                "doc_uuid_id": item.id, #item.uuid_id,
                "yeardate": item.yeardate,
                # "pdftmpfound": pdftmpfound,
                
        })
        if self.__request.method == 'POST':
            pass
        else:        
            self.__context = {
                                'appname': __package__.split('.')[1], 
                                'data': datalist,
                                'form': self.form
                            }
    @property
    def context(self):
        return self.__context
    @property
    def template_name(self):
        return self.__template_name
    @property
    def form(self):
        return self.__form

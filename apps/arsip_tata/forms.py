from django import forms
from django.core.exceptions import ValidationError
from .models import Year, Box, Bundle, Item, Bundlecode, Customer, Trans, TransDetail, Package, PackageItem
from django.core.exceptions import NON_FIELD_ERRORS
import re
# from django.forms import ModelForm

class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ['yeardate']

class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['box_number', 'yeardate', 'notes', 'token']
        error_messages = {
                    NON_FIELD_ERRORS: {
                        'unique_together': "Nomor Box Sudah Ada",
                    }
                }
    
class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = ['bundle_number', 'code', 'creator', 'description', 'year_bundle', 'yeardate', 'box', 'syncstatus']
        # fields = '__all__'
        error_messages = {
                    NON_FIELD_ERRORS: {
                        'unique_together': "Nomor Berkas Sudah Ada",
                    }
                }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     if not self.initial:
    #         yeardate = self.cleaned_data.get("yeardate")
    #         bundle_number = self.cleaned_data.get("bundle_number")

    #         searchbundle = Bundle.objects.filter(bundle_number=int(bundle_number), yeardate=int(yeardate))
    #         if searchbundle:
    #             raise ValidationError(f"No Berkas {bundle_number} pada Tahun Penataan {yeardate} Sudah Ada")
    #     return cleaned_data
    def clean(self):
        cleaned_data = super().clean()
        if not self.initial:
            yeardate = self.cleaned_data.get("yeardate")
            bundle_number = self.cleaned_data.get("bundle_number")
            if Bundle.objects.filter(bundle_number=bundle_number, yeardate=yeardate).count() != 0:
               cleaned_data['bundle_number'] = Bundle.objects.filter(yeardate=yeardate).latest('bundle_number').bundle_number + 1
        return cleaned_data

    
    def clean_code(self):
        cleaned_data = self.cleaned_data['code']
        bundlecode = Bundlecode.objects.filter(name__icontains=cleaned_data).first()
        if not bundlecode:
            raise ValidationError(f"Code tidak ada")
        code = bundlecode.name.split(" - ")[0]
        if cleaned_data != code:
            raise ValidationError(f"Code tidak ada")
        
        return code

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_number', 'title', 'copy', 'original', 'accesstype', 'yeardate', 'cover', 'bundle', 'token']
        error_messages = {
                    NON_FIELD_ERRORS: {
                        'unique_together': "Nomor Urut Sudah Ada",
                    }
                }
    
    def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data.get("copy") == 0 and self.cleaned_data.get("original") == 0:
            raise ValidationError(f"Jumlah Asli atau Jumlah Copy harus terisi")
        if not self.initial:
            yeardate = self.cleaned_data.get("yeardate")
            item_number = self.cleaned_data.get("item_number")
            if Item.objects.filter(item_number=item_number, yeardate=yeardate).count() != 0:
               cleaned_data['item_number'] = Item.objects.filter(yeardate=yeardate).latest('item_number').item_number + 1
        return cleaned_data
    
class CustomerForm(forms.ModelForm):
    # photo = forms.CharField(widget=forms.FileInput(attrs={'capture': "user"}))
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'description', 'photo', 'idcard', 'organization']

    def clean_phone_number(self):
        cleaned_data = self.cleaned_data['phone_number']
        if cleaned_data[0] == '0':
            cleaned_data = '+62' + cleaned_data[1:]
        reg = re.compile('^\+?1?\d{9,15}$')
        if not reg.match(cleaned_data):
            raise ValidationError(f"Format Telpon Salah, maximal 15 digit")
        
        return cleaned_data
        
class TransForm(forms.ModelForm):
    date_trans = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    class Meta:
        model = Trans
        fields = ['date_trans', 'customer']


class AddTransDetailForm(forms.Form): 
    code = forms.CharField(label="Kode Item Berkas", max_length = 255, help_text = "") 


class EditTransDetailForm(forms.ModelForm):
    date_return = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    class Meta:
        model = TransDetail
        fields = ['date_return']

class SearchItemForm(forms.Form): 
    title = forms.CharField(label="Judul", max_length = 255, help_text = "", required=False) 
    description = forms.CharField(label="Uraian Pekerjaan", max_length = 255, help_text = "", required=False) 

class SearchBundleForm(forms.Form): 
    search = forms.CharField(label="Uraian Pekerjaan", max_length = 255, help_text = "", required=False) 

class SearchDocByYear(forms.Form):
    search = forms.CharField(label="Kata Kunci")
    

class PackageForm(forms.ModelForm):
    date_send = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    class Meta:
        model=Package
        fields=('packnumber', 'date_send', 'count', 'name', 'position', 'organization', 'address')
        # widgets = {
        #     'name': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        #     'save_location': forms.Textarea(attrs={'cols': 80, 'rows': 4}),

        # }
        
        labels = {
            'name': 'Nama Pengirim',
            'packnumber': 'Nomor Dokumen',
            'date_send': 'Tanggal Pelaksanaan',
            'organization': 'Unit Kerja',
            'position': 'Jabatan',
            'address': 'Alamat',
            'count': 'Jumlah Box/Paket'

        }

class PackageItemForm(forms.ModelForm):
    class Meta:
        model = PackageItem
        fields = ['name', 'docnumber', 'docyear', 'count']
        labels = {
            'name': 'Nama Dokumen/Arsip',
            'docnumber': 'Nomor Dokumen',
            'docyear': 'Tahun',
            'count': 'Jumlah'

        }

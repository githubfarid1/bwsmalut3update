from django import forms
from django.core.exceptions import ValidationError
from .models import Year, Box, Bundle, Item, Bundlecode, Customer, Trans, TransDetail
from django.core.exceptions import NON_FIELD_ERRORS
import re

class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ['yeardate']

class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['box_number', 'yeardate']
        error_messages = {
                    NON_FIELD_ERRORS: {
                        'unique_together': "Nomor Box Sudah Ada",
                    }
                }
    
class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = ['bundle_number', 'code', 'creator', 'description', 'year_bundle', 'yeardate']

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
        fields = ['item_number', 'title', 'copy', 'original', 'accesstype', 'yeardate']
        error_messages = {
                    NON_FIELD_ERRORS: {
                        'unique_together': "Nomor Urut Sudah Ada",
                    }
                }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'description']

    def clean_phone_number(self):
        cleaned_data = self.cleaned_data['phone_number']
        reg = re.compile('^\+?1?\d{9,15}$')
        if not reg.match(cleaned_data):
            raise ValidationError(f"Format Telpon Salah, gunakan format +9999999, maximal 15 digit")
        
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
    description = forms.CharField(label="Uraian Masalah", max_length = 255, help_text = "", required=False) 
    title = forms.CharField(label="Judul", max_length = 255, help_text = "", required=False) 

from django import forms
from django.core.exceptions import ValidationError
from .models import Year, Box, Bundle, Item, Bundlecode
from django.core.exceptions import NON_FIELD_ERRORS

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
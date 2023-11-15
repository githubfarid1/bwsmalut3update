from django import forms
from .models import Variety, Doc
from django.forms import ModelForm


class SearchDoc(forms.Form):
    folder = forms.ModelChoiceField(
        queryset=Variety.objects.all(),
        widget=forms.Select(),
        to_field_name="folder",
        required=True, label="Jenis Dokumen"
    )
    search = forms.CharField(required=False, label="Keyword")


class InsertPdfDoc(forms.Form):
    folder = forms.ModelChoiceField(
        queryset=Variety.objects.all(),
        widget=forms.Select(),
        to_field_name="folder",
        required=True, label="Jenis Dokumen"
    )

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    filepath = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/pdf'}))
    uuid_id = forms.UUIDField(widget=forms.HiddenInput())


class DocAddForm(ModelForm):
    class Meta:
        model=Doc
        fields=('name', 'work_unit', 'period', 'media', 'countstr', 'save_life', 'save_location', 'protect_method', 'description')
        widgets = {
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
            'save_location': forms.Textarea(attrs={'cols': 80, 'rows': 4}),

        }
        labels = {
            'name': 'Nama Arsip',
            'work_unit': 'Unit Kerja',
            'period': 'Kurun Waktu',
            'media': 'Media',
            'countstr': 'Jumlah',
            'save_life': 'Jangka Simpan',
            'save_location': 'Lokasi Simpan',
            'protect_method': 'Metode Perlindungan',
            'description': 'Keterangan',

        }

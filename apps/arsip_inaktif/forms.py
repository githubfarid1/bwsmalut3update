from django import forms
from .models import Department, Doc
from django.forms import ModelForm
import calendar

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    filepath = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/pdf'}))
    uuid_id = forms.UUIDField(widget=forms.HiddenInput())

class DeletePdfFile(forms.Form):
    listdepartment = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(),
        to_field_name="name",
        required=True
    )
    box_number = forms.IntegerField(min_value=1) 
    doc_number = forms.IntegerField(min_value=1)

class SearchQRCodeForm(forms.Form): 
    qrcode = forms.CharField(label="QR Code", max_length = 255, help_text = "Search QR Code") 

class ListDocByBox(forms.Form):
    box_number = forms.IntegerField(min_value=1) 

class DeleteDoc(forms.Form):
    box_number = forms.IntegerField(min_value=1) 

class SearchDoc(forms.Form):
    folder = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(),
        to_field_name="folder",
        required=True, label="Kelompok"
    )
    search = forms.CharField()

class ExportForm(forms.Form):
    folder = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(),
        to_field_name="folder",
        required=True, label="Kelompok"
    )

class SearchDocByYear(forms.Form):
    search = forms.CharField(label="Kata Kunci")

class StatisticScan(forms.Form):
    month_choices = [(value, calendar.month_name[value]) for value in range(1, 13)]
    month = forms.ChoiceField(choices=month_choices)
    year = forms.IntegerField()

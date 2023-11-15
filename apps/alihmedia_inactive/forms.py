from django import forms
from .models import Department, Doc
from django.forms import ModelForm

# creating a form  


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



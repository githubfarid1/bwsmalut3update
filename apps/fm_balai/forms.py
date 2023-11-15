from django import forms
from .models import File, Department, Subfolder

class FileForm(forms.ModelForm):
    # fileupload = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept':'application/vnd.ms-excel, image/*, application/pdf, application/msword, application/vnd.ms-powerpoint, video/x-matroska, application/vnd.openxmlformats-officedocument.wordprocessingml.document, video/mp4'}))
    fileupload = forms.FileField(required=False, widget=forms.FileInput())
    class Meta:
        model = File
        fields = [
            # 'filename',
            'description',
            # 'tags',
        ]
        labels = {
                "description": "Deskripsi File",
        }

        widgets = {
            # 'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
            'description': forms.Textarea(attrs={'rows': '3'}),
            # 'filename': forms.FileInput(attrs={'accept':'application/vnd.ms-excel, image/*, application/pdf, application/msword, application/vnd.ms-powerpoint'})
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'name',
            'shortname',
        ]
        
        labels = {
                "name": "Nama PPK",
                "shortname": "Nama singkat"
        }

class SubfolderForm(forms.ModelForm):
    class Meta:
        model = Subfolder
        fields = [
            'name',
        ]
        labels = {
                "name": "Nama Folder",
        }

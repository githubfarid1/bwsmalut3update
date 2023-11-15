from django import forms
from .models import File, Department, Subfolder

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


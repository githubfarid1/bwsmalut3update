from django import forms
from .models import Department

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


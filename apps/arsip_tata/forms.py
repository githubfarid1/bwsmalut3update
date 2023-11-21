from django import forms

from .models import Year, Box, Bundle


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ['yeardate']

class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['box_number']

class BundleForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = ['bundle_number', 'code', 'creator', 'description', 'year_bundle']

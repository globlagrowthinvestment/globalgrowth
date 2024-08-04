from django import forms
from .models import Status, Package

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['package', 'image']
        widgets = {
            'package': forms.Select(), 
        }

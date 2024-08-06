from django import forms
from .models import Status, Package

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['image']  # Only include the image field
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}), 
        }


class PackagePurchaseForm(forms.Form):
    package = forms.ModelChoiceField(
        queryset=Package.objects.all(),
        required=True,
        widget=forms.RadioSelect
    )

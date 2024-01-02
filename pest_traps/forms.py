from django import forms
from .models import PestTrap

class PestTrapForm(forms.ModelForm):
    
    class Meta:
        model = PestTrap
        fields = ['name', 'token']
    
    
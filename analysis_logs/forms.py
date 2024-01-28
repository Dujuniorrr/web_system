from django import forms
from analysis_logs.models import AnalysisLog

class AnalysisLogForm(forms.ModelForm):
    
    class Meta:
        model = AnalysisLog
        fields = ['pests_number', 'temperature', 'pressure', 'date', 'processed_img_path', 'captured_img_path']
    
    
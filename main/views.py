from django.shortcuts import render
from analysis_logs.models import AnalysisLog
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'analysis_log/index.html', {'analysis_logs' : AnalysisLog.objects.all()})
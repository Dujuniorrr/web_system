from django.shortcuts import render
from accounts.models import ClientProfile
from analysis_logs.models import AnalysisLog
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from datetime import datetime, timedelta
from pest_traps.models import PestTrap
from django.contrib.auth.models import User


def handler404(request, exception, **kwargs):
    response = render(request, "error_pages/404.html")
    response.status_code = 404
    return response

def handler500(request, **kwargs):
    response = render(request, "error_pages/500.html")
    response.status_code = 500
    return response

@login_required
def home(request):
    
    user = request.user
    if request.user.is_superuser:
        user = ClientProfile.objects.get(request.GET.get('user')).user if request.GET.get('user') else  ClientProfile.objects.filter(user__is_active=True).first().user
        
    last_week = datetime.today() - timedelta(days=7)
    
    total_pests = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=user),
        date__gte=last_week, 
        date__lte=datetime.today()
    ).aggregate(Sum('pests_number'))['pests_number__sum']
    
    avg_temperature  = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=user),
        date__gte=last_week,
        date__lte=datetime.today()
    ).aggregate(Avg('temperature'))['temperature__avg']
    
    avg_pressure  = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=user),
        date__gte=last_week, 
        date__lte=datetime.today()
    ).aggregate(Avg('pressure'))['pressure__avg'] 
    
    records = len(AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=user),
        date__gte=last_week, 
        date__lte=datetime.today()))
    
    return render(request, 'main/index.html', {
        'total_pests' : total_pests if total_pests else 0,
        'temperature': round(avg_temperature, 2) if avg_temperature else 0,
        'pressure': round(avg_pressure, 2)  if avg_pressure else 0,
        'records': records,
        'users':  ClientProfile.objects.filter(user__is_active=True)
    })
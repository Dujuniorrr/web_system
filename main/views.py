from django.http import JsonResponse
from django.shortcuts import render
from analysis_logs.models import AnalysisLog
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from pest_traps.models import PestTrap


def get_number_pests_by_day(request):
    last_week = datetime.today() - timedelta(days=7)
    
    pests_by_day = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=request.user),
        date__gte=last_week,
        date__lte=datetime.today()
    ).annotate(day_of_week=ExtractWeekDay('date')) 

    aggregated_results = pests_by_day.values('day_of_week').annotate(total_pests=Sum('pests_number'))
    
    print(aggregated_results)

    return JsonResponse({
       
    })
     

@login_required
def home(request):
    last_week = datetime.today() - timedelta(days=7)
    
    total_pests = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=request.user),
        date__gte=last_week, 
        date__lte=datetime.today()
    ).aggregate(Sum('pests_number'))['pests_number__sum']
    
    avg_temperature  = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=request.user),
        date__gte=last_week,
        date__lte=datetime.today()
    ).aggregate(Avg('temperature'))['temperature__avg']
    
    avg_pressure  = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=request.user),
        date__gte=last_week, 
        date__lte=datetime.today()
    ).aggregate(Avg('pressure'))['pressure__avg'] 
    
    records = len(AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=request.user),
        date__gte=last_week, 
        date__lte=datetime.today()))
    
    return render(request, 'main/index.html', {
        'total_pests' : total_pests if total_pests else 0,
        'temperature': round(avg_temperature, 2) if avg_temperature else 0,
        'pressure': round(avg_pressure, 2)  if avg_pressure else 0,
        'records': records,
    })
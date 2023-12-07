from django.shortcuts import render
from analysis_logs.models import AnalysisLog
from pest_traps.models import PestTrap
from django.http import JsonResponse
from analysis_logs.models import AnalysisLog
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime, timedelta
from django.db.models import Sum, F
from django.db.models.functions import ExtractWeekDay
from pest_traps.models import PestTrap

days_dict = {
    1: 'Domingo',
    2: 'Segunda-Feira',
    3: 'Terça-Feira',
    4: 'Quarta-Feira',
    5: 'Quinta-Feira',
    6: 'Sexta-Feira',
    7: 'Sábado',
}

def get_number_pests_by_day(request):
    last_week = datetime.today() - timedelta(days=7)
    
    pests_by_day = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=request.user),
        date__gte=last_week,
        date__lte=datetime.today()
    ).annotate(day_of_week=ExtractWeekDay('date')) 

    aggregated_results = pests_by_day.values('day_of_week').annotate(total_pests=Sum('pests_number'))
    
    days = []
    total_pests = []
  
    for pest_by_day in aggregated_results:
        days.append(days_dict[pest_by_day['day_of_week']])
        total_pests.append(pest_by_day['total_pests'])
        
    return JsonResponse({
       'days': days,
       'total_pests': total_pests
    })
    
@login_required
def index(request, id=None):
    if id:
        pest_trap = PestTrap.objects.get(id=id, user=request.user)
    else:
        pest_trap = PestTrap.objects.filter(user=request.user).first()
        
    return render(request, 'analysis_log/index.html', {
        'analysis_logs' : AnalysisLog.objects.filter(pest_trap=PestTrap.objects.get(id=pest_trap.id)),
        'pest_traps': PestTrap.objects.filter(user=request.user).exclude(id=pest_trap.id),
        'pest_trap' : pest_trap
    })
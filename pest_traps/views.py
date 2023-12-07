from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum, Avg
from analysis_logs.models import AnalysisLog
from .models import PestTrap
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'pest_traps/index.html', {
        'traps': PestTrap.objects.filter(user=request.user)
    })
    
@login_required
def get_grouped_traps(request):
    last_week = datetime.today() - timedelta(days=7)
     
    grouped_traps = AnalysisLog.objects.filter(
       pest_trap__in=PestTrap.objects.filter(user=request.user),
        date__gte=last_week, date__lte=datetime.today()
    ).values('pest_trap__name').annotate(total_pests=Sum('pests_number'))
    
    names = []
    total_pests  = []

    for trap in grouped_traps:
        names.append('Armadilha ' + trap['pest_trap__name'])
        total_pests.append(trap['total_pests'])
    
    return JsonResponse({
        'names': names,
        'total_pests' : total_pests
    })

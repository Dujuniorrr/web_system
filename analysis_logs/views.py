from django.shortcuts import redirect, render
from accounts.models import ClientProfile
from analysis_logs.forms import AnalysisLogForm
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
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from web_system.utils import do_pagination
from django.db.models import Avg

days_dict = {
    1: 'Domingo',
    2: 'Segunda-Feira',
    3: 'Terça-Feira',
    4: 'Quarta-Feira',
    5: 'Quinta-Feira',
    6: 'Sexta-Feira',
    7: 'Sábado',
}

@login_required
def get_data_by_day(request):
    user = request.user
    if request.user.is_superuser:
        user = ClientProfile.objects.get(user_id=request.GET.get('user')).user if request.GET.get('user') else  ClientProfile.objects.filter(user__is_active=True).first().user
        
    today = datetime.today()
    last_week = today - timedelta(days=7)
    # last_week_start = today - timedelta(days=today.weekday() + 14)
    # last_week_end = last_week_start + timedelta(days=6)

    data_by_day = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=user),
        # date__gte=last_week_start,
        # date__lte=last_week_end
        date__gte=last_week,
        date__lte=today
    ).annotate(day_of_week=ExtractWeekDay('date')) 

    aggregated_results = data_by_day.values('day_of_week').annotate(
        total_pests=Sum('pests_number'),
        avg_temperature=Avg('temperature'),
        avg_pressure=Avg('pressure')
    ).order_by('-day_of_week')  
    
    days = []
    total_pests = []
    avg_temperatures = []
    avg_pressures = []
  
    for data_day in aggregated_results:
        days.append(days_dict[data_day['day_of_week']])
        total_pests.append(data_day['total_pests'])
        avg_temperatures.append(data_day['avg_temperature'])
        avg_pressures.append(data_day['avg_pressure'])
    
    return JsonResponse({
       'days': days,
       'total_pests': total_pests,
       'avg_temperatures': avg_temperatures,
       'avg_pressures': avg_pressures
    })

@login_required
def get_number_pests_by_day(request):
    user = request.user
    if request.user.is_superuser:
        user = ClientProfile.objects.get(user_id=request.GET.get('user')).user if request.GET.get('user') else  ClientProfile.objects.filter(user__is_active=True).first().user
        
    last_week = datetime.today() - timedelta(days=7)
    
    pests_by_day = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=user),
        date__gte=last_week,
        date__lte=datetime.today()
    ).annotate(day_of_week=ExtractWeekDay('date')) 

    aggregated_results = pests_by_day.values('day_of_week').annotate(total_pests=Sum('pests_number')).order_by('-day_of_week')  
    
    days = []
    total_pests = []
  
    for pest_by_day in aggregated_results:
        days.append(days_dict[pest_by_day['day_of_week']])
        total_pests.append(pest_by_day['total_pests'])
        
    return JsonResponse({
       'days': days,
       'total_pests': total_pests
    })
    
@csrf_exempt
def receive_analysis_log_data(request):
   try:
        if request.method == 'POST':
            print(request.POST)
            form = AnalysisLogForm(request.POST, request.FILES)
            pest_trap = PestTrap.objects.get(token=request.POST.get('pest_trap_token'))
            print(pest_trap)
            if form.is_valid() and pest_trap and pest_trap.is_active:
                analysis_log = form.save(commit=False)
                analysis_log.pest_trap = pest_trap
                analysis_log.save()
                return JsonResponse({'success': True}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Armadilha desativada'}, status=400)
                
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        
   except:
        return JsonResponse({'success': False}, status=405)
       
@login_required
def index(request, id=None):
    if id and not request.user.is_superuser:
        pest_trap = PestTrap.objects.filter(id=id, user=request.user).first()
        
    elif id and request.user.is_superuser:
         pest_trap = PestTrap.objects.filter(id=id).first()
         
    elif request.user.is_superuser:
        pest_trap = PestTrap.objects.filter().first()

    else:
        pest_trap = PestTrap.objects.filter(user=request.user).first()

    analysis_logs = []
    pest_traps = []
    if pest_trap:

        if request.user.is_superuser:
            pest_traps = PestTrap.objects.filter(user=pest_trap.user).exclude(id=pest_trap.id, is_active=False)
            
        else:
            pest_traps = PestTrap.objects.filter(user=request.user).exclude(id=pest_trap.id, is_active=False)
    
        analysis_logs = AnalysisLog.objects.filter(pest_trap=PestTrap.objects.get(id= pest_trap.id))
        
        search = request.GET.get('searchField', None)
        if search:
            search = float(search) 

            analysis_logs = analysis_logs.filter(
                Q(pests_number__contains=str(int(search))) |
                Q(pressure__contains=str(int(search))) |
                Q(temperature__contains=str(int(search))) |
                Q(pressure__contains=str(search)) |
                Q(temperature__contains=str(search))
            )
        
        params_mapping = {
            'initial_date': 'date__gte',
            'final_date': 'date__lte',
            'min_pest': 'pests_number__gte',
            'max_pest': 'pests_number__lte',
            'min_temperature': 'temperature__gte',
            'max_temperature': 'temperature__lte',
            'min_pressure': 'pressure__gte',
            'max_pressure': 'pressure__lte',
        }

        filters = {params_mapping[key]: request.GET[key] for key in params_mapping if request.GET.get(key)}

        try:
            if filters:
                analysis_logs = analysis_logs.filter(Q(**filters))
                
        except Exception as e:
            print('error: ' + str(e))
        
    context =  {
        'pest_traps': pest_traps,
        'pest_trap' : pest_trap
    }
    
    if analysis_logs.__class__ != list:
        analysis_logs = analysis_logs.order_by('-date')
   
    context.update(
         do_pagination(
            request.GET.get('page') if request.GET.get('page') else 1,
            'analysis_logs', analysis_logs, 20)
    )

    return render(request, 'analysis_log/index.html', context)
    
    

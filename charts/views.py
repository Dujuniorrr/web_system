from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Min, Max
from datetime import datetime, timedelta
from analysis_logs.models import AnalysisLog
from pest_traps.models import PestTrap
from django.db.models.functions import TruncDate
from django.db.models import Avg

def index(request):
    return render(request, 'charts/index.html')

def line_chart_number_of_pests(request):
    params_mapping = {
        'initial_date': 'date__gte',
        'final_date': 'date__lte',
    }

    filters = {params_mapping[key]: request.GET[key] for key in params_mapping if request.GET.get(key)}

    queryset = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=request.user),
        **filters
    ).annotate(truncated_date=TruncDate('date')).values('truncated_date').annotate(total_pests=Sum('pests_number')).order_by('truncated_date')

    number_pests = {
        'min_pest': 'total_pests__gte',
        'max_pest': 'total_pests__lte',
    }
    
    filters = {number_pests[key]: request.GET[key] for key in number_pests if request.GET.get(key)}
    
    queryset = queryset.filter(**filters)
    

    data = {
        'labels': [entry['truncated_date'].strftime('%d/%m/%Y') for entry in queryset],
        'data': [entry['total_pests'] for entry in queryset],
    }
    
    return JsonResponse(data)


def line_chart_average_temperature(request):
    params_mapping = {
        'initial_date': 'date__gte',
        'final_date': 'date__lte',
    }

    filters = {params_mapping[key]: request.GET[key] for key in params_mapping if request.GET.get(key)}

    queryset = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=request.user),
        **filters
    ).annotate(truncated_date=TruncDate('date')).values('truncated_date').annotate(avg_temperature=Avg('temperature')).order_by('truncated_date')

    number_pests = {
        'min_temperature': 'avg_temperature__gte',
        'max_temperature': 'avg_temperature__lte',
    }
    
    filters = {number_pests[key]: request.GET[key] for key in number_pests if request.GET.get(key)}
    
    queryset = queryset.filter(**filters)
    

    data = {
          'labels': [entry['truncated_date'].strftime('%d/%m/%Y') for entry in queryset],
        'data': [entry['avg_temperature'] for entry in queryset],
    }
    
    return JsonResponse(data)

def line_chart_average_pressure(request):
    params_mapping = {
        'initial_date': 'date__gte',
        'final_date': 'date__lte',
    }

    filters = {params_mapping[key]: request.GET[key] for key in params_mapping if request.GET.get(key)}

    queryset = AnalysisLog.objects.filter(
        pest_trap__in=PestTrap.objects.filter(user=request.user),
        **filters
    ).annotate(truncated_date=TruncDate('date')).values('truncated_date').annotate(avg_pressure=Avg('pressure')).order_by('truncated_date')

    number_pests = {
        'min_pressure': 'avg_pressure__gte',
        'max_pressure': 'avg_pressure__lte',
    }
    
    filters = {number_pests[key]: request.GET[key] for key in number_pests if request.GET.get(key)}
    
    queryset = queryset.filter(**filters)
    

    data = {
        'labels': [entry['truncated_date'].strftime('%d/%m/%Y') for entry in queryset],

        'data': [entry['avg_pressure'] for entry in queryset],
    }
    
    return JsonResponse(data)

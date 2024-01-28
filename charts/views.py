from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.utils import timezone
from analysis_logs.models import AnalysisLog
from pest_traps.models import PestTrap
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear
from django.db.models import Avg
# from django.contrib.auth.decorators import login_required
from web_system.utils import only_client_permited
from datetime import datetime

@only_client_permited
def index(request):
    return render(request, 'charts/index.html', {
        'pest_traps': PestTrap.objects.filter(user=request.user, analysislog__isnull=False ).distinct(),
        'years': reversed(list(range(request.user.date_joined.year, datetime.now().year + 1)))
    })


@only_client_permited
def column_chart_number_of_pests(request):
    def calculate_weekly_pests(month, year, pest_trap_filter):
        queryset = AnalysisLog.objects.filter(
            pest_trap_filter,
            date__month=month,
            date__year=year
        ).annotate(
            truncated_week=TruncWeek('date'),
            truncated_month=TruncMonth('date')
        ).values('truncated_week').annotate(total_pests=Sum('pests_number')).order_by('truncated_week')

        weekly_pests = {
            'labels': [entry['truncated_week'].strftime('%d/%m/%Y') for entry in queryset],
            'data': [round(entry['total_pests'], 2) for entry in queryset],
        }

        return weekly_pests

    pest_trap_id = request.GET.get('pest_trap_column')
    pest_trap_filter = Q(pest_trap__in=PestTrap.objects.filter(user=request.user))
    if pest_trap_id:
        pest_trap_filter = Q(pest_trap_id=pest_trap_id)

    now = timezone.now()
    default_month = now.month - 1 if now.month > 1 else 12
    default_year = now.year if now.month > 1 else now.year - 1

    
    month = int(request.GET.get('monthColumn', default_month))
    year = int(request.GET.get('yearColumn', default_year))
    
    print('\n' + request.GET.get('monthColumn'))
    print('\n' + request.GET.get('yearColumn'))
    # print('\n' + str(month))

    weekly_pests_data = calculate_weekly_pests(month, year, pest_trap_filter)

    data = {
        'labels': weekly_pests_data['labels'],
        'data': weekly_pests_data['data'],
    }

    return JsonResponse(data)

@only_client_permited
def column_chart_average_temperature(request):
    def calculate_weekly_average_temperature(month, year, pest_trap_filter):
        queryset = AnalysisLog.objects.filter(
            pest_trap_filter,
            date__month=month,
            date__year=year
        ).annotate(
            truncated_week=TruncWeek('date'),
            truncated_month=TruncMonth('date')
        ).values('truncated_week').annotate(avg_temperature=Avg('temperature')).order_by('truncated_week')

        weekly_avg_temperature = {
            'labels': [entry['truncated_week'].strftime('%d/%m/%Y') for entry in queryset],
            'data': [round(entry['avg_temperature'], 2) for entry in queryset],
        }

        return weekly_avg_temperature

    pest_trap_id = request.GET.get('pest_trap_column')
    pest_trap_filter = Q(pest_trap__in=PestTrap.objects.filter(user=request.user))
    if pest_trap_id:
        pest_trap_filter = Q(pest_trap_id=pest_trap_id)

    now = timezone.now()
    default_month = now.month - 1 if now.month > 1 else 12
    default_year = now.year if now.month > 1 else now.year - 1

    month = int(request.GET.get('monthColumn', default_month))
    year = int(request.GET.get('yearColumn', default_year))

    weekly_avg_temperature_data = calculate_weekly_average_temperature(month, year, pest_trap_filter)

    data = {
        'labels': weekly_avg_temperature_data['labels'],
        'data': weekly_avg_temperature_data['data'],
    }

    return JsonResponse(data)

@only_client_permited
def column_chart_average_pressure(request):
    def calculate_weekly_average_pressure(month, year, pest_trap_filter):
        queryset = AnalysisLog.objects.filter(
            pest_trap_filter,
            date__month=month,
            date__year=year
        ).annotate(
            truncated_week=TruncWeek('date'),
            truncated_month=TruncMonth('date')
        ).values('truncated_week').annotate(avg_pressure=Avg('pressure')).order_by('truncated_week')

        weekly_avg_pressure = {
            'labels': [entry['truncated_week'].strftime('%d/%m/%Y') for entry in queryset],
            'data': [round(entry['avg_pressure'], 2) for entry in queryset],
        }

        return weekly_avg_pressure

    pest_trap_id = request.GET.get('pest_trap_column')
    pest_trap_filter = Q(pest_trap__in=PestTrap.objects.filter(user=request.user))
    if pest_trap_id:
        pest_trap_filter = Q(pest_trap_id=pest_trap_id)

    now = timezone.now()
    default_month = now.month - 1 if now.month > 1 else 12
    default_year = now.year if now.month > 1 else now.year - 1

    month = int(request.GET.get('monthColumn', default_month))
    year = int(request.GET.get('yearColumn', default_year))

    weekly_avg_pressure_data = calculate_weekly_average_pressure(month, year, pest_trap_filter)

    data = {
        'labels': weekly_avg_pressure_data['labels'],
        'data': weekly_avg_pressure_data['data'],
    }


    return JsonResponse(data)

@only_client_permited
def line_chart_number_of_pests(request):
    params_mapping = {
        'initial_date': 'date__gte',
        'final_date': 'date__lte',
    }
    
    date_mapping = {
        'day': TruncDate('date'),
        'week': TruncWeek('date'),
        'month': TruncMonth('date'),
        'year': TruncYear('date'),
    }

    filters = {params_mapping[key]: request.GET[key] for key in params_mapping if request.GET.get(key)}

    pest_trap_id = request.GET.get('pest_trap')
    pest_trap_filter = Q(pest_trap__in=PestTrap.objects.filter(user=request.user))
    if pest_trap_id:
        pest_trap_filter = Q(pest_trap_id=pest_trap_id)
    
    queryset = AnalysisLog.objects.filter(
        pest_trap_filter,
        **filters
    ).annotate(truncated_date=date_mapping.get(
        request.GET.get('dateColumn', 'day')
    )).values('truncated_date').annotate(total_pests=Sum('pests_number')).order_by('truncated_date')
    
    
    number_pests = {
        'min_value': 'total_pests__gte',
        'max_value': 'total_pests__lte',
    }

    filters = {number_pests[key]: request.GET[key] for key in number_pests if request.GET.get(key)}

    queryset = queryset.filter(**filters)

    data = {
        'labels': [entry['truncated_date'].strftime('%d/%m/%Y') for entry in queryset],
        'data': [entry['total_pests'] for entry in queryset],
    }

    return JsonResponse(data)

@only_client_permited
def line_chart_average_temperature(request):
    params_mapping = {
        'initial_date': 'date__gte',
        'final_date': 'date__lte',
    }

    date_mapping = {
        'day': TruncDate('date'),
        'week': TruncWeek('date'),
        'month': TruncMonth('date'),

        'year': TruncYear('date')
    }

    filters = {params_mapping[key]: request.GET[key] for key in params_mapping if request.GET.get(key)}

    pest_trap_id = request.GET.get('pest_trap')
    pest_trap_filter = Q(pest_trap__in=PestTrap.objects.filter(user=request.user))
    if pest_trap_id:
        pest_trap_filter = Q(pest_trap_id=pest_trap_id)

    queryset = AnalysisLog.objects.filter(
        pest_trap_filter,
        **filters
    ).annotate(truncated_date=date_mapping.get(
        request.GET.get('dateColumn', 'day')
    )).values('truncated_date').annotate(avg_temperature=Avg('temperature')).order_by('truncated_date')

    number_pests = {
        'min_value': 'avg_temperature__gte',
        'max_value': 'avg_temperature__lte',
    }

    filters = {number_pests[key]: request.GET[key] for key in number_pests if request.GET.get(key)}

    queryset = queryset.filter(**filters)

    data = {
        'labels': [entry['truncated_date'].strftime('%d/%m/%Y') for entry in queryset],
        'data': [round(entry['avg_temperature'], 2) for entry in queryset],
    }

    return JsonResponse(data)

@only_client_permited
def line_chart_average_pressure(request):
    params_mapping = {
        'initial_date': 'date__gte',
        'final_date': 'date__lte',
    }
    
    date_mapping = {
        'day': TruncDate('date'),
        'week': TruncWeek('date'),
        'month': TruncMonth('date'),
        'year': TruncYear('date')
    }

    filters = {params_mapping[key]: request.GET[key] for key in params_mapping if request.GET.get(key)}

    pest_trap_id = request.GET.get('pest_trap')
    pest_trap_filter = Q(pest_trap__in=PestTrap.objects.filter(user=request.user))
    if pest_trap_id:
        pest_trap_filter = Q(pest_trap_id=pest_trap_id)

    queryset = AnalysisLog.objects.filter(
        pest_trap_filter,
        **filters
    ).annotate(truncated_date=date_mapping.get(
        request.GET.get('dateColumn', 'day')
    )).values('truncated_date').annotate(avg_pressure=Avg('pressure')).order_by('truncated_date')

    number_pests = {
        'min_value': 'avg_pressure__gte',
        'max_value': 'avg_pressure__lte',
    }

    filters = {number_pests[key]: request.GET[key] for key in number_pests if request.GET.get(key)}

    queryset = queryset.filter(**filters)

    data = {
        'labels': [entry['truncated_date'].strftime('%d/%m/%Y') for entry in queryset],
        'data': [round(entry['avg_pressure'], 2) for entry in queryset],
    }

    return JsonResponse(data)

@only_client_permited
def scatter_chart(request):
    params_mapping = {
        'initialDate': 'date__gte',
        'finalDate': 'date__lte',
    }
    
    date_mapping = {
        'day': TruncDate('date'),
        'week': TruncWeek('date'),
        'month': TruncMonth('date'),
        'year': TruncYear('date')
    }

    filters = {params_mapping[key]: request.GET[key] for key in params_mapping if request.GET.get(key)}

    pest_trap_id = request.GET.get('pest_trap')
    pest_trap_filter = Q(pest_trap__in=PestTrap.objects.filter(user=request.user))
    if pest_trap_id:
        pest_trap_filter = Q(pest_trap_id=pest_trap_id)

    queryset = AnalysisLog.objects.filter(
        pest_trap_filter,
        **filters
    ).annotate(truncated_date= date_mapping.get(
        request.GET.get('date_column', 'day')
    )).values('truncated_date').annotate(avg=Avg(request.GET.get('xVariable', 'temperature')), total_pests=Sum('pests_number')).order_by('truncated_date')

    number_pests = {
        'min_value': 'avg__gte',
        'max_value': 'avg__lte',
    }

    filters = {number_pests[key]: request.GET[key] for key in number_pests if request.GET.get(key)}

    queryset = queryset.filter(**filters)

    data = {
        'labels': [entry['truncated_date'].strftime('%d/%m/%Y') for entry in queryset],
        'data': [{'x': round(entry['avg'], 2), 'y': entry['total_pests']} for entry in queryset],
        # 'x': [ round(entry['avg_pressure'], 2) for entry in queryset],
        # 'y': [ entry['total_pests'] for entry in queryset],
    }
    
    print(data)
    return JsonResponse(data)

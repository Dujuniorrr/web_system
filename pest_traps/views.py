from datetime import datetime, timedelta
import uuid
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db.models import Sum, Avg
from accounts.models import ClientProfile
from analysis_logs.models import AnalysisLog
from pest_traps.forms import PestTrapForm
from .models import PestTrap
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from web_system.utils import do_pagination, superuser_required

@login_required
def index(request):
    status_mapping = {
        '1': True,
        '2': False,
    }

    status = status_mapping.get(request.GET.get('status'))
    print(status)
    traps = PestTrap.objects.filter(user=request.user, user__is_active=True) if not request.user.is_superuser else PestTrap.objects.filter(user__is_active=True)

    if status is not None:
        traps = traps.filter(is_active=status)

    username_param = request.GET.get('username')
    if username_param and not username_param == '*' and request.user.is_superuser:
        user_instance = User.objects.filter(id=username_param).first()
        traps = traps.filter(user=user_instance)

    context = {
        'users': ClientProfile.objects.filter(user__is_active=True)
    }
    context.update(do_pagination(
        request.GET.get('page') if request.GET.get('page') else 1, 'traps', traps, 10
    ))
    print(context)
    return render(request, 'pest_traps/index.html', context)
    
@superuser_required
def generate_token(request):
    try:
        user = User.objects.get(id=request.GET.get('id'))
        pest_traps = PestTrap.objects.filter(user=user)
        return JsonResponse({
            'name': f'Armadilha { len(list(pest_traps)) + 1}',
            'token': str(uuid.uuid4())
        })
        
    except:
        return JsonResponse({'success': False, 'message': 'Usuário não existe'})
   
@superuser_required
def desactive_pest_trap(request, id):
    if request.method == 'POST':
        try:
            pest_trap = PestTrap.objects.get(id=id)
            if pest_trap.is_active:
                pest_trap.is_active = False
                pest_trap.save()
                return JsonResponse({'success': True, 'message': f'{pest_trap.name} de {pest_trap.user.first_name} {pest_trap.user.last_name} foi desativada!'})
            return JsonResponse({'success': True, 'message': f'{pest_trap.name} de {pest_trap.user.first_name} {pest_trap.user.last_name} já está desativada!'})
        except PestTrap.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Essa armadilha não existe!'})
    return redirect('/')

@superuser_required
def active_pest_trap(request, id):
    if request.method == 'POST':
        try:
            pest_trap = PestTrap.objects.get(id=id)
            if not pest_trap.is_active:
                pest_trap.is_active = True
                pest_trap.save()
                return JsonResponse({'success': True, 'message': f'{pest_trap.name} de {pest_trap.user.first_name} {pest_trap.user.last_name} foi ativada!'})
            return JsonResponse({'success': True, 'message': f'{pest_trap.name} de {pest_trap.user.first_name} {pest_trap.user.last_name} já está ativa!'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Essa armadilha não existe!'})
    return redirect('/')

@login_required
def create_pest_trap(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            form = PestTrapForm(request.POST)
            if form.is_valid():
                pest_trap = form.save(commit=False)
                pest_trap.token = request.POST.get('token')
                pest_trap.user = User.objects.get(id=request.POST.get('username'))
                pest_trap.save()
                return JsonResponse({'success': True})  
            else:
                return JsonResponse({'success': False, 
                                'errors': form.errors.as_json(), 
                                'form_data': form.cleaned_data})  
        else:
            return redirect('/')
    except Exception as e:
        return JsonResponse({'success': False, 
                            'alert_in_modal' : True, 
                            'error':'O tipo de usuário informado é inválido!'})
        
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
        names.append(trap['pest_trap__name'])
        total_pests.append(trap['total_pests'])
    
    return JsonResponse({
        'names': names,
        'total_pests' : total_pests
    })

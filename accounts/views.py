from django.http import  JsonResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import ImageProfileForm, UserCreateForm, ClientProfileForm, PasswordChangeFormCustom
from django.contrib.auth.models import User
from web_system.utils import do_pagination, superuser_required
from .models import ClientProfile
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q

@superuser_required
def register_user(request):
    forms = {'admin': UserCreateForm, 'client': ClientProfileForm}  
    if request.method == 'POST':  
        if request.POST.get('type') in ['admin', 'client']:
            form = forms[request.POST.get('type')](request.POST)
            if form.is_valid():
                form.save(True)
                return JsonResponse({'success': True})  
            else:
                return JsonResponse({'success': False, 
                             'errors': form.errors.as_json(), 
                             'form_data': form.cleaned_data})  
        else:            
            return JsonResponse({'success': False, 
                                'alert_in_modal' : True, 
                                'error':'O tipo de usuário informado é inválido!'})
    return redirect('/')

@superuser_required
def desactive_user(request, id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=id)
            if user.is_active:
                user.is_active = False
                user.save()
                return JsonResponse({'success': True, 'message': f'{user.first_name} {user.last_name} foi desativado!'})
            return JsonResponse({'success': True, 'message': f'{user.first_name} {user.last_name} já está desativado!'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Esse usuário não existe!'})
    return redirect('/')

@superuser_required
def active_user(request, id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=id)
            if not user.is_active:
                user.is_active = True
                user.save()
                return JsonResponse({'success': True, 'message': f'{user.first_name} {user.last_name} foi ativado!'})
            return JsonResponse({'success': True, 'message': f'{user.first_name} {user.last_name} já está ativo!'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Esse usuário não existe!'})
    return redirect('/')

@superuser_required
def list_users(request):
    users = User.objects.all()
     
    search = request.GET.get('searchField', None)
    if search:
        users = users.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(clientprofile__cpf__icontains=search) |
            Q(clientprofile__address__icontains=search) |
            Q(clientprofile__phone__icontains=search) 
        )
    
    params_mapping = {
        'first_name': 'first_name__icontains',
        'last_name': 'last_name__icontains',
        'email': 'email__icontains',
        'cpf': 'clientprofile__cpf__icontains',
        'address': 'clientprofile__address__icontains',
        'phone': 'clientprofile__phone__icontains',
        'date': 'clientprofile__date',
    }

    filters = {params_mapping[key]: request.GET[key] for key in params_mapping if request.GET.get(key)}

    try:
        if filters:
            users = users.filter(Q(**filters))
            
    except Exception as e:
        print('error: ' + str(e))
        
    status_mapping = {
        '1': True,
        '2': False,
    }

    status = status_mapping.get(request.GET.get('status'))
    if status is not None:
        users = users.filter(is_active=status)
        
    context = {
        'form': UserCreateForm(), 
        'client_form': ClientProfileForm(), 
    }
    context.update(do_pagination(
    request.GET.get('page') if request.GET.get('page') else 1,
    'users',  users, 20))
    return render(request, 'accounts/index.html', context)

@login_required
def show_profile(request):
    profile = None
    client_form = None
    if ClientProfile.objects.filter(user=request.user).exists():
        profile = ClientProfile.objects.get(user=request.user)
        client_form = ClientProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {
        'profile' : profile,
        'form': UserCreateForm(instance=request.user), 
        'img_form' : ImageProfileForm,
        'change_password_form': PasswordChangeFormCustom(user=request.user),
        'client_form': client_form})

@login_required
def edit_profile(request):
    instaces = {'admin': request.user}
    forms = {'admin': UserCreateForm, 'client': ClientProfileForm}  
    if request.method == 'POST':  
        if request.POST.get('type') == 'client':
            instaces['client'] = ClientProfile.objects.get(user=request.user)
        if request.POST.get('type') in ['admin', 'client']:
            form = forms[request.POST.get('type')](request.POST, instance=instaces[request.POST.get('type')])
            if form.is_valid():
                form.save(update=True)
                return JsonResponse({'success': True, 'message': 'Informações atualizadas!'})  
            
            return JsonResponse({'success': False, 
                             'errors': form.errors.as_json(), 
                             'form_data': form.cleaned_data})  
        else:            
            return JsonResponse({'success': False, 
                                'alert_in_modal' : True, 
                                'error':'O tipo de usuário informado é inválido!'})
    return redirect('/')

@login_required()
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeFormCustom(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'success': True, 'message': 'Senha alterada!'})  
        else:
            return JsonResponse({'success': False, 
                            'errors': form.errors.as_json(), 
                            'form_data': form.cleaned_data})  
    return redirect('/')

@login_required()
def update_image(request):
    if request.method == 'POST':
        form = ImageProfileForm(request.POST, request.FILES, instance=request.user.clientprofile)
        print(request.FILES)
        if form.is_valid():
            user = form.save()
            return JsonResponse({'success': True, 
                                 'message': 'Imagem de perfil alterada!',
                                 'img_path': user.img_path.url})  
        else:
            return JsonResponse({'success': False, 
                            'message': 'Apenas arquivos em formatos de imagens são aceitos!'})  
    return redirect('/')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:    
            return redirect('home')
        return super().get(request, *args, **kwargs)

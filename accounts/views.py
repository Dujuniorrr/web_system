from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .forms import UserCreateForm, ClientProfileForm
from django.contrib.auth.models import User
from web_system.utils import superuser_required

@login_required
@superuser_required
def register_user(request):
    forms = {'admin': UserCreateForm, 'client': ClientProfileForm}  
    if request.method == 'POST':  
        if request.POST.get('type') in ['admin', 'client']:
            form = forms[request.POST.get('type')](request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})  
            else:
                return JsonResponse({'success': False, 
                             'errors': form.errors.as_json(), 
                             'form_data': form.cleaned_data})  
        else:
            print('test')
            
            return JsonResponse({'success': False, 
                                'alert_in_modal' : True, 
                                'error':'O tipo de usuário informado é inválido!'})
    print('test')
    
    return JsonResponse({'success': False, 'message': 'Método de requisição inválido!'})

@login_required
@superuser_required
def desactive_user(request):
    # if 
    pass

@login_required
@superuser_required
def active_user(request):
    pass

@login_required
@superuser_required
def list_users(request):
    return render(request, 'accounts/index.html', {
        'form': UserCreateForm(), 
        'client_form': ClientProfileForm(),
        'users' : User.objects.all()
    })

@login_required
def show_profile(request):
    pass

@login_required
def edit_profile(request):
    pass

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:    
            return redirect('home')

        return super().get(request, *args, **kwargs)

from datetime import datetime
from typing import Any
from django import forms
from django.contrib.auth.models import User
from .models import ClientProfile
import uuid
from web_system.utils import send_code_by_email
from django.contrib.auth.hashers import make_password

class UserCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        label="Nome",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    
    last_name = forms.CharField(
        required=True,
        label="Sobrenome",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))

    email = forms.EmailField(
        required=True,
        label="Email", 
        widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
    
    def is_valid(self) -> bool:
        super().is_valid()
        if self.cleaned_data.get('email') and User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', 'Já existe um usuário com este e-mail.')
       
        return  super().is_valid()

    def save(self, commit: bool = ...,  by_child = False) -> Any:
        if by_child:
            return super().save(commit)
        
        instance = super().save(False)
        instance.username = instance.first_name + instance.last_name + str(uuid.uuid4())
        
        code = str(uuid.uuid4())
        instance.password = make_password(code)
        print(code)
        send_code_by_email(instance, code)
        
        instance.is_superuser = True

        if commit:
            instance.save() 
       
        return instance
        
class ClientProfileForm(UserCreateForm):
    cpf = forms.CharField(
        required=True,
        label="CPF",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'maxlength':11}))
    
    phone = forms.CharField(
        required=True,
        label="Telefone",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'maxlenght':19}))
    
    address = forms.CharField(
        required=True,
        label="Endereço",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    
    birthday = forms.DateField(
        required=True,
        
        label="Data de Nascimento",
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type':'date'}))
    
    class Meta:
        model = ClientProfile
        fields = ['email', 'first_name', 'last_name', 'cpf', 'phone', 'address', 'birthday']
    
    def clean_birthday(self):
        data = self.cleaned_data['birthday']
    
        today = datetime.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        print(age)
        if age <= 18:
            raise forms.ValidationError(f'A idade mínima para cadastro de usuário é 18 anos.')
            
        return data
        
    def clean_phone(self):
        data = self.cleaned_data['phone']
        if len(data) < 19:
            raise forms.ValidationError(f'O campo deve ter no mínimo 19 caracteres.')
        return data
    
    def clean_cpf(self):
        data = self.cleaned_data['cpf']
        if len(data) < 14:
            raise forms.ValidationError(f'O campo deve ter no mínimo 14 caracteres.')
        return data
    
    def save(self,  commit: bool = ...) -> Any:
        instance = super().save(False, by_child=True) 
        user = UserCreateForm(self.cleaned_data).save(commit=False)
        user.is_superuser = False
        user.save()
        instance.user = user

        if commit:         
            instance.save()
            
        return instance
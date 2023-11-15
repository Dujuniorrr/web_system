from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    cpf = models.CharField(max_length=14, verbose_name="CPF", null=False)
    phone = models.CharField(max_length=19, verbose_name="Telefone", null=False)
    address = models.TextField(verbose_name="Endereço", null=False)
    birthday = models.DateField(verbose_name="Data de Aniversário", null=False)
    img_path = models.ImageField(verbose_name="Imagem de Perfil", upload_to="profile_imgs/", null=False, default='profile_imgs/icon-profile.png')
    code_to_password = models.CharField(max_length=255, verbose_name="Código", null=False)
    
    class Meta:
        verbose_name = "Cliente"
        
    def __str__(self) -> str:
        return f'{self.user.first_name} ({self.cpf})'

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

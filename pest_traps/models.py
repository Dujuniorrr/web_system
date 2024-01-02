import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PestTrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=16, verbose_name="Nome", null=False)
    is_active = models.BooleanField(verbose_name="Ativo", default=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    token = models.UUIDField( default = uuid.uuid4) 
    
    class Meta:
        verbose_name = "Armadilha"
        
    def __str__(self) -> str:
        return f'{self.name} - Dono: {self.user.first_name})'
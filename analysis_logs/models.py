from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from pest_traps.models import PestTrap

class AnalysisLog(models.Model):
    pest_trap = models.ForeignKey(PestTrap, on_delete=models.CASCADE, null=False)
    pests_number = models.IntegerField(verbose_name="Número de Pragas", null=False)
    temperature = models.FloatField(verbose_name="Temperatura", null=False)
    pressure = models.FloatField(verbose_name="Pressão Atmósferica", null=False)
    date = models.DateTimeField(verbose_name="Data de Captura", null=False)
    processed_img_path = models.ImageField(verbose_name="Imagem Processada", upload_to="processed_imgs/", null=False)
    captured_img_path = models.ImageField(verbose_name="Imagem Capturada", upload_to="captured_imgs/", null=False)
    
    class Meta:
        verbose_name = "Monitoramento"
        
    def __str__(self) -> str:
        return f'Monitoramento ({self.date}'
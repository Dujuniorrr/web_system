# Generated by Django 3.2.8 on 2023-11-11 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=14, verbose_name='CPF')),
                ('phone', models.CharField(max_length=19, verbose_name='Telefone')),
                ('address', models.TextField(verbose_name='Endereço')),
                ('birthday', models.DateField(verbose_name='Data de Aniversário')),
                ('img_path', models.ImageField(default='profile_imgs/icon-profile.png', upload_to='profile_imgs/', verbose_name='Imagem de Perfil')),
                ('code_to_password', models.CharField(max_length=255, verbose_name='Código')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cliente',
            },
        ),
    ]

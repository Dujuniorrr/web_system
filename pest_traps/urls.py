from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list'),
    path('cadastrar', views.create_pest_trap, name='add'),
    path('agrupar', views.get_grouped_traps, name='grouped_traps'),
    path('gerar-token', views.generate_token, name='generate_token'),
    path('ativar/<int:id>', views.active_pest_trap, name='active'),
    path('desativar/<int:id>', views.desactive_pest_trap, name='desactive'),
]
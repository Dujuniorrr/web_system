from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list'),
    path('agrupar', views.get_grouped_traps, name='grouped_traps')
]
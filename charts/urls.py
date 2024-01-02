from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list'),
    path('linha/numero-de-pragas', views.line_chart_number_of_pests, name='list'),
    path('linha/media-de-temperatura', views.line_chart_average_temperature, name='list'),
    path('linha/media-de-pressao', views.line_chart_average_pressure, name='list'),
]
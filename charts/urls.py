from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list'),
    path('linha/numero-de-pragas', views.line_chart_number_of_pests, name='line_pest'),
    path('linha/media-de-temperatura', views.line_chart_average_temperature, name='line_temp'),
    path('linha/media-de-pressao', views.line_chart_average_pressure, name='line_pressure'),
    path('coluna/numero-de-pragas', views.column_chart_number_of_pests, name='column_pest'),
    path('coluna/media-de-temperatura', views.column_chart_average_temperature, name='column_pest'),
    path('coluna/media-de-pressao', views.column_chart_average_pressure, name='column_pest'),
    path('dispersao', views.scatter_chart, name='column_pest'),
]
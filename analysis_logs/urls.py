from django.urls import path
from analysis_logs import views

urlpatterns = [
    path('', views.index, name='list'),
    path('<int:id>', views.index, name='list'),
    path('semana/dias', views.get_number_pests_by_day, name='days_of_week'),
    path('semana/dias/linha', views.get_data_by_day, name='days_of_week'),
    path('webhook', views.receive_analysis_log_data, name='webhook'),
]
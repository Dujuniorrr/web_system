from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_users, name='list'), #,4
    path('login/', views.CustomLoginView.as_view(), name="login",  kwargs={'redirect_authenticated_user': True}), 
    path('cadastrar', views.register_user, name='register_user'), 
    path('desativar/<int:id>', views.desactive_user, name='desactive_user'), # 2
    path('ativar/<int:id>', views.active_user, name='active_user'), # 3
    path('perfil', views.show_profile, name='show_profile'), # 5
    path('editar', views.edit_profile, name="edit_profile") # 6
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_users, name='list'), 
    path('login/', views.CustomLoginView.as_view(), name="login",  kwargs={'redirect_authenticated_user': True}), 
    path('cadastrar', views.register_user, name='register_user'), 
    path('desativar/<int:id>', views.desactive_user, name='desactive_user'), 
    path('ativar/<int:id>', views.active_user, name='active_user'), 
    path('perfil', views.show_profile, name='show_profile'),
    path('editar', views.edit_profile, name="edit_profile"),
    path('mudar-senha', views.change_password, name="change_password"),
    path('alterar-imagem', views.update_image, name="change_password")
    
]

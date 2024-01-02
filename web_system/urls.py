from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from main.views import handler404, handler500

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('armadilhas/', include('pest_traps.urls')),
    path('monitoramentos/', include('analysis_logs.urls')),
    path('usuarios/', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
    path('usuarios/', include("django.contrib.auth.urls")),
    path('graficos/', include("charts.urls")),
    
    path('password-reset/', PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        html_email_template_name='registration/password_reset_email.html'
        ), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    
]


handler404 = handler404
handler500 = handler500

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
document_root=settings.STATIC_ROOT)
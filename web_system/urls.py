from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('armadilhas/', include('pest_traps.urls')),
    path('monitoramentos/', include('analysis_logs.urls')),
    path('usuarios/', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
    path('usuarios/', include("django.contrib.auth.urls"))
]

import django.contrib.auth.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
document_root=settings.STATIC_ROOT)
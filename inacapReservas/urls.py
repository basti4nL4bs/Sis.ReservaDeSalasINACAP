from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/', include('django.contrib.auth.urls')),  # Proporciona /cuentas/login/ y logout/
    path('', include('salas.urls')),
]
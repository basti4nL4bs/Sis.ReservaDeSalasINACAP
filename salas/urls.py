from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

app_name = 'salas'

# Router oficial de Django REST Framework
router = DefaultRouter()
router.register(r'salas', api_views.SalaViewSet, basename='api-salas')
router.register(r'reservas', api_views.ReservaViewSet, basename='api-reservas')

urlpatterns = [
    # --- ENDPOINTS API RESTFUL (Unidad 3) ---
    path('api/', include(router.urls)),
    path('api/token/', api_views.CustomAuthToken.as_view(), name='api-token'),

    # --- RUTAS FRONTEND WEB (MVT) ---
    path('', views.index, name='index'),
    path('<int:sala_id>/', views.detail, name='detail'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('<int:sala_id>/reservar/', views.crear_reserva, name='crear_reserva'),
    path('reserva/<int:reserva_id>/editar/', views.editar_reserva, name='editar_reserva'),
    path('reserva/<int:reserva_id>/eliminar/', views.eliminar_reserva, name='eliminar_reserva'),
]
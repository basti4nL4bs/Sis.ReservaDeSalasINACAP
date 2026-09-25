from django.urls import path
from . import views

app_name = 'salas'

urlpatterns = [
    # READ
    path('', views.index, name='index'),
    path('<int:sala_id>/', views.detail, name='detail'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),

    # CREATE
    path('<int:sala_id>/reservar/', views.crear_reserva, name='crear_reserva'),

    # UPDATE
    path('reserva/<int:reserva_id>/editar/', views.editar_reserva, name='editar_reserva'),

    # DELETE
    path('reserva/<int:reserva_id>/eliminar/', views.eliminar_reserva, name='eliminar_reserva'),
]
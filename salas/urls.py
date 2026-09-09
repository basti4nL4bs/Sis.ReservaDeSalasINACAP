from django.urls import path
from . import views

app_name = 'salas'

urlpatterns = [
    path('', views.index, name='index'),                                # /
    path('<int:sala_id>/', views.detail, name='detail'),               # /5/
    path('<int:sala_id>/reservar/', views.reservar, name='reservar'),   # /5/reservar/
    path('<int:sala_id>/results/', views.results, name='results'),     # /5/results/
]
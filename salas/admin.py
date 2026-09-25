from django.contrib import admin
from .models import Sala, Reserva

@admin.action(description='Marcar reservas seleccionadas como Confirmadas')
def marcar_confirmadas(modeladmin, request, queryset):
    queryset.update(estado='CONFIRMADA')

@admin.action(description='Marcar reservas seleccionadas como Canceladas')
def marcar_canceladas(modeladmin, request, queryset):
    queryset.update(estado='CANCELADA')

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'capacidad', 'activa', 'total_reservas')
    list_filter = ('tipo', 'activa')
    search_fields = ('nombre',)
    list_editable = ('activa',)

    @admin.display(description='Reservas Registradas')
    def total_reservas(self, obj):
        return obj.reservas.count()

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('sala', 'usuario', 'fecha', 'hora_inicio', 'hora_fin', 'estado')
    list_filter = ('estado', 'fecha', 'sala__tipo')
    search_fields = ('sala__nombre', 'usuario__username', 'motivo')
    date_hierarchy = 'fecha'
    ordering = ('-fecha', '-hora_inicio')
    actions = [marcar_confirmadas, marcar_canceladas]
from django.contrib import admin
from .models import SalaEstudio, BloqueHorario

class BloqueHorarioInline(admin.TabularInline):
    model = BloqueHorario
    extra = 3

class SalaEstudioAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Identificación del Espacio", {"fields": ["codigo", "edificio", "piso"]}),
        ("Capacidad y Estado", {"fields": ["capacidad", "activa"]}),
    ]
    inlines = [BloqueHorarioInline]
    list_display = ("codigo", "edificio", "piso", "capacidad", "activa")
    list_filter = ["activa", "piso", "edificio"]
    search_fields = ["codigo", "edificio"]

admin.site.register(SalaEstudio, SalaEstudioAdmin)
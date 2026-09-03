from django.db import models


class SalaEstudio(models.Model):
    codigo = models.CharField(max_length=20, help_text="Ej: Sala Cowork A-214 Taller 3")
    edificio = models.CharField(max_length=50, default="Edificio A")
    piso = models.IntegerField(default=2)
    capacidad = models.PositiveBigIntegerField(default=6)
    activa = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.codigo} (piso {self.piso} - Capacidad: {self.capacidad} personas.)"

class BloqueHorario(models.Model):
    sala = models.ForeignKey(SalaEstudio, on_delete=models.CASCADE, related_name="bloques")
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estudiante_rut = models.CharField(max_length=12, blank=True, null=True, help_text="RUT del alumno que reserva")
    estudiante_nombre = models.CharField(max_length=100, blank=True, null=True)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    esta_reservado = models.BooleanField(default=False)

    def __str__(self):
        estado = f"Ocupado por {self.estudiante_nombre}" if self.esta_reservado else "Disponible"
        return f"{self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')} [{estado}]"
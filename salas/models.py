from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Sala(models.Model):
    TIPO_SALA = [
        ('LAB', 'Laboratorio de Computación'),
        ('TEO', 'Sala Teórica'),
        ('AUD', 'Auditorio'),
    ]

    nombre = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=3, choices=TIPO_SALA, default='TEO')
    capacidad = models.PositiveIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Reserva(models.Model):
    ESTADOS = [
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='CONFIRMADA')

    def __str__(self):
        return f"{self.sala.nombre} - {self.fecha} ({self.hora_inicio} a {self.hora_fin})"

    def clean(self):
        super().clean()
        # Validación de rango de horas
        if self.hora_inicio and self.hora_fin:
            if self.hora_inicio >= self.hora_fin:
                raise ValidationError({'hora_fin': 'La hora de término debe ser posterior a la de inicio.'})

        # Validación de solapamiento de horarios en la misma sala
        if self.sala_id and self.fecha and self.hora_inicio and self.hora_fin:
            solapadas = Reserva.objects.filter(
                sala=self.sala,
                fecha=self.fecha,
                estado='CONFIRMADA',
                hora_inicio__lt=self.hora_fin,
                hora_fin__gt=self.hora_inicio
            )
            if self.pk:
                solapadas = solapadas.exclude(pk=self.pk)
            if solapadas.exists():
                raise ValidationError(f"La sala {self.sala.nombre} ya tiene una reserva en ese horario.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
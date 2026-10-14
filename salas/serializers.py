from rest_framework import serializers
from .models import Sala, Reserva

class SalaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    total_reservas = serializers.SerializerMethodField()

    class Meta:
        model = Sala
        fields = ['id', 'nombre', 'tipo', 'tipo_display', 'capacidad', 'activa', 'total_reservas']

    def get_total_reservas(self, obj):
        return obj.reservas.count()


class ReservaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')
    sala_nombre = serializers.ReadOnlyField(source='sala.nombre')

    class Meta:
        model = Reserva
        fields = [
            'id', 'sala', 'sala_nombre', 'usuario', 'usuario_nombre',
            'fecha', 'hora_inicio', 'hora_fin', 'motivo', 'estado'
        ]
        read_only_fields = ['usuario', 'estado']

    def validate(self, attrs):
        hora_inicio = attrs.get('hora_inicio') or getattr(self.instance, 'hora_inicio', None)
        hora_fin = attrs.get('hora_fin') or getattr(self.instance, 'hora_fin', None)
        fecha = attrs.get('fecha') or getattr(self.instance, 'fecha', None)
        sala = attrs.get('sala') or getattr(self.instance, 'sala', None)

        # Regla 1: Secuencia horaria
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError({
                "hora_fin": "La hora de término debe ser estrictamente posterior a la de inicio."
            })

        # Regla 2: Anti-solapamiento en la misma sala y fecha
        if sala and fecha and hora_inicio and hora_fin:
            solapadas = Reserva.objects.filter(
                sala=sala,
                fecha=fecha,
                estado='CONFIRMADA',
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            )
            if self.instance:
                solapadas = solapadas.exclude(pk=self.instance.pk)

            if solapadas.exists():
                raise serializers.ValidationError({
                    "non_field_errors": ["La sala ya cuenta con una reserva activa en ese rango de horario."]
                })

        return attrs
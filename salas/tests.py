from django.test import TestCase
from django.urls import reverse
from .models import SalaEstudio, BloqueHorario
import datetime

class SalaModelTests(TestCase):
    def test_sala_creacion(self):
        sala = SalaEstudio.objects.create(codigo="Sala A-101", capacidad=6)
        self.assertEqual(str(sala), "Sala A-101 (Piso 1 - Capacidad: 6 pers.)")


class ReservaViewTests(TestCase):
    def test_index_sin_salas(self):
        response = self.client.get(reverse("salas:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay salas de estudio habilitadas")

    def test_reserva_post_exitosa(self):
        sala = SalaEstudio.objects.create(codigo="Sala B-202", capacidad=4)
        bloque = BloqueHorario.objects.create(
            sala=sala,
            hora_inicio=datetime.time(10, 0),
            hora_fin=datetime.time(11, 0),
        )

        response = self.client.post(
            reverse("salas:reservar", args=(sala.id,)),
            {
                "bloque": bloque.id,
                "rut": "12345678-9",
                "nombre": "Estudiante Prueba",
                "carrera": "Analista Programador",
            },
        )

        bloque.refresh_from_db()
        self.assertTrue(bloque.esta_reservado)
        self.assertEqual(bloque.estudiante_nombre, "Estudiante Prueba")
        self.assertRedirects(response, reverse("salas:results", args=(sala.id,)))
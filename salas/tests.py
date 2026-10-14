from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Sala, Reserva

class APIRestfulTests(APITestCase):
    def setUp(self):
        # Usuario común
        self.user = User.objects.create_user(username='alumno_api', password='password123')
        self.token, _ = Token.objects.get_or_create(user=self.user)

        # Usuario administrador
        self.admin = User.objects.create_superuser(username='admin_api', password='password123')
        self.admin_token, _ = Token.objects.get_or_create(user=self.admin)

        # Segundo usuario (para verificar aislamiento de datos)
        self.other_user = User.objects.create_user(username='otro_alumno', password='password123')
        self.other_token, _ = Token.objects.get_or_create(user=self.other_user)

        # Sala de pruebas
        self.sala = Sala.objects.create(
            nombre='Laboratorio Redes',
            tipo='LAB',
            capacidad=25,
            activa=True
        )

    def test_01_listar_salas_publico(self):
        """GET /api/salas/ responde 200 OK en formato JSON sin necesidad de token."""
        url = reverse('salas:api-salas-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], 'Laboratorio Redes')

    def test_02_obtener_token_autenticacion(self):
        """POST /api/token/ con credenciales entrega el token de acceso seguro."""
        url = reverse('salas:api-token')
        data = {'username': 'alumno_api', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'alumno_api')

    def test_03_crear_reserva_sin_token_falla(self):
        """POST /api/reservas/ sin autenticación responde 401 Unauthorized."""
        url = reverse('salas:api-reservas-list')
        data = {
            'sala': self.sala.id,
            'fecha': '2026-11-20',
            'hora_inicio': '10:00:00',
            'hora_fin': '11:30:00',
            'motivo': 'Prueba sin login'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_04_crear_reserva_con_token_exitoso(self):
        """POST /api/reservas/ con Token válido responde 201 Created y asocia al usuario autenticado."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('salas:api-reservas-list')
        data = {
            'sala': self.sala.id,
            'fecha': '2026-11-20',
            'hora_inicio': '10:00:00',
            'hora_fin': '11:30:00',
            'motivo': 'Taller Redes con Token'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['usuario_nombre'], 'alumno_api')

    def test_05_solapamiento_horario_rechazado_api(self):
        """POST /api/reservas/ con colisión de horarios responde 400 Bad Request."""
        Reserva.objects.create(
            sala=self.sala,
            usuario=self.user,
            fecha='2026-11-20',
            hora_inicio='10:00:00',
            hora_fin='11:30:00',
            motivo='Reserva inicial',
            estado='CONFIRMADA'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('salas:api-reservas-list')
        data = {
            'sala': self.sala.id,
            'fecha': '2026-11-20',
            'hora_inicio': '10:30:00',
            'hora_fin': '12:00:00',
            'motivo': 'Reserva colisionante'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_06_usuario_no_puede_acceder_a_reserva_ajena(self):
        """Aislamiento de datos: un usuario no puede consultar ni alterar reservas ajenas."""
        reserva_user1 = Reserva.objects.create(
            sala=self.sala,
            usuario=self.user,
            fecha='2026-11-21',
            hora_inicio='09:00:00',
            hora_fin='10:30:00',
            motivo='Reserva privada user 1',
            estado='CONFIRMADA'
        )
        # El otro usuario intenta acceder al endpoint directo de la reserva
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        url = reverse('salas:api-reservas-detail', args=[reserva_user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
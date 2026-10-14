from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import Sala, Reserva
from .serializers import SalaSerializer, ReservaSerializer
from .permissions import IsOwnerOrAdmin, IsAdminUserOrReadOnly

class CustomAuthToken(ObtainAuthToken):
    """
    POST /api/token/
    Recibe username y password en formato JSON y retorna el Token seguro de acceso.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'is_staff': user.is_staff
        }, status=status.HTTP_200_OK)


class SalaViewSet(viewsets.ModelViewSet):
    """
    API RESTful de Salas:
    - GET /api/salas/ (Listado público)
    - POST /api/salas/ (Solo Admin)
    - GET /api/salas/{id}/ (Detalle público)
    - PUT/PATCH /api/salas/{id}/ (Solo Admin)
    - DELETE /api/salas/{id}/ (Solo Admin)
    """
    serializer_class = SalaSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Sala.objects.all()
        return Sala.objects.filter(activa=True)


class ReservaViewSet(viewsets.ModelViewSet):
    """
    API RESTful de Reservas (Privada por Token):
    - GET /api/reservas/ (Lista solo reservas del usuario autenticado)
    - POST /api/reservas/ (Crea reserva vinculada al usuario del token)
    - GET /api/reservas/{id}/ (Detalle protegido)
    - PUT/PATCH /api/reservas/{id}/ (Modificación protegida)
    - DELETE /api/reservas/{id}/ (Cancelación protegida)
    """
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return Reserva.objects.none()
        if user.is_staff:
            return Reserva.objects.all()
        return Reserva.objects.filter(usuario=user)

    def perform_create(self, serializer):
        # Asignación forzada del usuario autenticado vía token
        serializer.save(usuario=self.request.user)
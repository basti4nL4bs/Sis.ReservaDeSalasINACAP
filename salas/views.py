from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Sala, Reserva

def index(request):
    """Paso 1: Lista las salas disponibles."""
    salas_disponibles = Sala.objects.filter(activa=True)
    return render(request, 'salas/index.html', {'salas': salas_disponibles})

def detail(request, sala_id):
    """Paso 2: Muestra la ficha de la sala y el formulario para agendar."""
    sala = get_object_or_404(Sala, pk=sala_id, activa=True)
    return render(request, 'salas/detail.html', {'sala': sala})

def reservar(request, sala_id):
    """Paso 3: Procesa el POST (igual que 'vote' en el tutorial oficial)."""
    sala = get_object_or_404(Sala, pk=sala_id)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        motivo = request.POST.get('motivo', '')

        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para agendar.")
            return redirect('salas:detail', sala_id=sala.id)

        try:
            nueva_reserva = Reserva(
                sala=sala,
                usuario=request.user,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                motivo=motivo
            )
            nueva_reserva.save() # Ejecuta el método clean() del modelo
            # Redirección POST exitosa para evitar reenvío duplicado
            return HttpResponseRedirect(reverse('salas:results', args=(sala.id,)))
        except Exception as error:
            messages.error(request, f"Error en la reserva: {error}")
            return redirect('salas:detail', sala_id=sala.id)

    return redirect('salas:detail', sala_id=sala.id)

def results(request, sala_id):
    """Paso 4: Muestra el resultado/historial tras reservar."""
    sala = get_object_or_404(Sala, pk=sala_id)
    reservas = sala.reservas.filter(estado='CONFIRMADA')
    return render(request, 'salas/results.html', {'sala': sala, 'reservas': reservas})
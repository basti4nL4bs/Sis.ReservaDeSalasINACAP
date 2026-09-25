from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib import messages
from .models import Sala, Reserva
from .forms import ReservaForm

# READ: Catálogo público de salas disponibles
def index(request):
    salas_disponibles = Sala.objects.filter(activa=True)
    return render(request, 'salas/index.html', {'salas': salas_disponibles})

# READ: Detalle de la sala
def detail(request, sala_id):
    sala = get_object_or_404(Sala, pk=sala_id, activa=True)
    reservas_activas = sala.reservas.filter(estado='CONFIRMADA')
    return render(request, 'salas/detail.html', {'sala': sala, 'reservas': reservas_activas})

# READ: Listado de reservas del usuario en sesión
@login_required
def mis_reservas(request):
    reservas_usuario = Reserva.objects.filter(usuario=request.user)
    return render(request, 'salas/mis_reservas.html', {'reservas': reservas_usuario})

# CREATE: Crear reserva desde detail.html
@login_required
def crear_reserva(request, sala_id):
    sala = get_object_or_404(Sala, pk=sala_id, activa=True)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.sala = sala
            reserva.usuario = request.user
            try:
                reserva.full_clean()
                reserva.save()
                messages.success(request, f"¡Reserva en {sala.nombre} confirmada con éxito!")
                return redirect('salas:mis_reservas')
            except ValidationError as e:
                error_msg = e.message_dict.get('__all__', [str(e)])[0] if hasattr(e, 'message_dict') else str(e)
                messages.error(request, error_msg)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

        return redirect('salas:detail', sala_id=sala.id)

    return redirect('salas:detail', sala_id=sala.id)

# UPDATE: Editar reserva existente
@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    if reserva.usuario != request.user and not request.user.is_staff:
        raise PermissionDenied("No tienes permiso para modificar esta reserva.")

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            try:
                reserva_editada = form.save(commit=False)
                reserva_editada.full_clean()
                reserva_editada.save()
                messages.success(request, "Reserva actualizada con éxito.")
                return redirect('salas:mis_reservas')
            except ValidationError as e:
                error_msg = e.message_dict.get('__all__', [str(e)])[0] if hasattr(e, 'message_dict') else str(e)
                messages.error(request, error_msg)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'salas/form_reserva.html', {'form': form, 'sala': reserva.sala, 'modo': 'Editar'})

# DELETE: Eliminar una reserva
@login_required
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    if reserva.usuario != request.user and not request.user.is_staff:
        raise PermissionDenied("No tienes permiso para eliminar esta reserva.")

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "La reserva ha sido eliminada correctamente.")
        return redirect('salas:mis_reservas')

    return render(request, 'salas/confirmar_eliminar.html', {'reserva': reserva})
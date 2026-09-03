from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import SalaEstudio, BloqueHorario

class IndexView(generic.ListView):
    template_name = "salas/index.html"
    context_object_name = "lista_salas"

    def get_queryset(self):
        return SalaEstudio.objects.filter(activa=True).order_by("piso", "codigo")

class DetailView(generic.DetailView):
    model = SalaEstudio
    template_name = "salas/detail.html"

class ResultsView(generic.DetailView):
    model = SalaEstudio
    template_name = "salas/results.html"

def reservar_bloque(request, sala_id):
    sala = get_object_or_404(SalaEstudio, pk=sala_id)
    try:
        bloque_seleccionado = sala.bloques.get(pk=request.POST["bloque"])
    except (KeyError, BloqueHorario.DoesNotExist):
        return render(
            request,
            "salas/detail.html",
            {
                "salaestudio": sala,
                "error_message": "Debes seleccionar un bloque horario válido para reservar.",
            },
        )
    else:
        if bloque_seleccionado.esta_reservado:
            return render(
                request,
                "salas/detail.html",
                {
                    "salaestudio": sala,
                    "error_message": "Este bloque ya fue reservado por otro estudiante.",
                },
            )

        rut = request.POST.get("rut", "").strip()
        nombre = request.POST.get("nombre", "").strip()
        carrera = request.POST.get("carrera", "").strip()

        if not rut or not nombre:
            return render(
                request,
                "salas/detail.html",
                {
                    "salaestudio": sala,
                    "error_message": "El RUT y Nombre son obligatorios.",
                },
            )

        bloque_seleccionado.estudiante_rut = rut
        bloque_seleccionado.estudiante_nombre = nombre
        bloque_seleccionado.carrera = carrera
        bloque_seleccionado.esta_reservado = True
        bloque_seleccionado.save()

        return HttpResponseRedirect(reverse("salas:results", args=(sala.id,)))
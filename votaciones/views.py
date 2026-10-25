from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from inertia import render

from catalogo.models import Opcion, Votacion
from catalogo.serializers import opcion_payload, votacion_payload
from resultados.services import puede_ver_resultados_publicos

from .models import Voto
from .services import VotoError, emitir_voto


@login_required
def confirmar(request, votacion_id):
    votacion = get_object_or_404(Votacion, pk=votacion_id)
    opcion_id = request.GET.get("opcion")
    opcion = get_object_or_404(Opcion, pk=opcion_id, votacion=votacion)
    if votacion.estado_efectivo() != "abierta":
        messages.error(request, "Esta votación no está disponible.")
        return redirect("votacion_detalle", votacion_id=votacion.pk)
    return render(
        request,
        "Votaciones/Confirmar",
        {
            "votacion": votacion_payload(votacion),
            "opcion": opcion_payload(opcion),
        },
    )


@login_required
def votar(request, votacion_id):
    if request.method != "POST":
        return redirect("votacion_opciones", votacion_id=votacion_id)
    votacion = get_object_or_404(Votacion, pk=votacion_id)
    opcion = get_object_or_404(Opcion, pk=request.POST.get("opcion_id"), votacion=votacion)
    if request.POST.get("confirmado") != "1":
        messages.error(request, "Debes confirmar que no podrás modificar el voto.")
        return redirect(f"{reverse('voto_confirmar', args=[votacion.pk])}?opcion={opcion.pk}")
    try:
        emitir_voto(request.user, votacion, opcion)
    except VotoError as exc:
        messages.error(request, exc.mensaje)
        return redirect("votacion_detalle", votacion_id=votacion.pk)
    messages.success(request, "Tu voto quedó guardado.")
    return redirect("voto_gracias", votacion_id=votacion.pk)


@login_required
def gracias(request, votacion_id):
    votacion = get_object_or_404(Votacion, pk=votacion_id)
    ya_voto = Voto.objects.filter(usuario=request.user, votacion=votacion).exists()
    return render(
        request,
        "Votaciones/Gracias",
        {
            "votacion": votacion_payload(votacion),
            "puede_ver_resultados": puede_ver_resultados_publicos(votacion),
            "ya_voto": ya_voto,
        },
    )

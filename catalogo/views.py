from django.shortcuts import get_object_or_404, redirect
from inertia import render

from .models import Categoria, Edicion, Votacion
from .serializers import categoria_payload, opcion_payload, votacion_payload


def _edicion_activa():
    return Edicion.objects.filter(estado=Edicion.Estado.ACTIVA).order_by("-anio").first()


def inicio(request):
    return render(request, "Publico/Inicio")


def categorias(request):
    edicion = _edicion_activa()
    items = []
    if edicion:
        items = [
            categoria_payload(categoria)
            for categoria in edicion.categorias.filter(estado=Categoria.Estado.ACTIVA)
        ]
    return render(request, "Publico/Categorias", {"categorias": items})


def votaciones(request, categoria_id):
    categoria = get_object_or_404(
        Categoria.objects.select_related("edicion"),
        pk=categoria_id,
        estado=Categoria.Estado.ACTIVA,
    )
    items = [
        votacion_payload(votacion)
        for votacion in categoria.votaciones.exclude(estado=Votacion.Estado.BORRADOR)
    ]
    return render(
        request,
        "Publico/Votaciones",
        {"categoria": categoria_payload(categoria), "votaciones": items},
    )


def detalle(request, votacion_id):
    votacion = get_object_or_404(
        Votacion.objects.select_related("categoria"),
        pk=votacion_id,
    )
    if votacion.estado == Votacion.Estado.BORRADOR:
        return redirect("categorias")
    return render(
        request,
        "Publico/Detalle",
        {
            "votacion": votacion_payload(votacion),
            "categoria": categoria_payload(votacion.categoria),
        },
    )


def opciones(request, votacion_id):
    votacion = get_object_or_404(
        Votacion.objects.select_related("categoria").prefetch_related("opciones"),
        pk=votacion_id,
    )
    if votacion.estado_efectivo() != "abierta":
        return redirect("votacion_detalle", votacion_id=votacion.pk)
    return render(
        request,
        "Publico/Opciones",
        {
            "votacion": votacion_payload(votacion),
            "opciones": [opcion_payload(opcion) for opcion in votacion.opciones.all()],
        },
    )

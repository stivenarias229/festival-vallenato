from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from inertia import render

from .models import Categoria, Edicion, Opcion, Votacion
from .serializers import categoria_payload, opcion_payload, votacion_payload


def _edicion_activa():
    return Edicion.objects.filter(estado=Edicion.Estado.ACTIVA).order_by("-anio").first()


def api_categorias(_request):
    """GET /api/categorias/ — categorías con votaciones y opciones (entrega Eje 3)."""
    edicion = _edicion_activa()
    categorias = []
    if edicion:
        queryset = (
            edicion.categorias.filter(estado=Categoria.Estado.ACTIVA)
            .prefetch_related(
                Prefetch(
                    "votaciones",
                    queryset=Votacion.objects.exclude(estado=Votacion.Estado.BORRADOR)
                    .prefetch_related(
                        Prefetch(
                            "opciones",
                            queryset=Opcion.objects.order_by("orden", "id"),
                        )
                    )
                    .order_by("id"),
                )
            )
            .order_by("id")
        )
        for categoria in queryset:
            categorias.append(
                {
                    **categoria_payload(categoria),
                    "votaciones": [
                        {
                            **votacion_payload(votacion),
                            "opciones": [opcion_payload(opcion) for opcion in votacion.opciones.all()],
                        }
                        for votacion in categoria.votaciones.all()
                    ],
                }
            )
    return JsonResponse({"categorias": categorias})


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

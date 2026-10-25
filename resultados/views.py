import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from inertia import render

from auditoria.services import registrar_auditoria
from catalogo.models import Votacion
from catalogo.serializers import votacion_payload
from cuentas.permissions import requiere_administrador

from .services import agregar_resultados, puede_ver_resultados_publicos


def publicos(request, votacion_id):
    votacion = get_object_or_404(Votacion, pk=votacion_id)
    if not puede_ver_resultados_publicos(votacion):
        return render(
            request,
            "Resultados/Publicos",
            {
                "votacion": votacion_payload(votacion),
                "disponible": False,
                "resultados": {"total": 0, "opciones": []},
            },
        )
    return render(
        request,
        "Resultados/Publicos",
        {
            "votacion": votacion_payload(votacion),
            "disponible": True,
            "resultados": agregar_resultados(votacion),
        },
    )


@requiere_administrador
def admin(request):
    votaciones = Votacion.objects.select_related("categoria").exclude(
        estado=Votacion.Estado.BORRADOR
    )
    seleccion_id = request.GET.get("votacion")
    votacion = None
    if seleccion_id:
        votacion = get_object_or_404(votaciones, pk=seleccion_id)
    elif votaciones.exists():
        votacion = votaciones.first()
    if votacion:
        registrar_auditoria(
            request.user,
            "consultar_resultados",
            "votacion",
            f"Consultó resultados de {votacion.titulo}.",
        )
    return render(
        request,
        "Panel/Resultados",
        {
            "votaciones": [votacion_payload(item) for item in votaciones],
            "votacion": votacion_payload(votacion) if votacion else None,
            "resultados": agregar_resultados(votacion) if votacion else {"total": 0, "opciones": []},
        },
    )


@requiere_administrador
def exportar_csv(request, votacion_id):
    votacion = get_object_or_404(Votacion, pk=votacion_id)
    datos = agregar_resultados(votacion)
    registrar_auditoria(
        request.user,
        "exportar_resultados",
        "votacion",
        f"Exportó CSV de {votacion.titulo}.",
    )
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="resultados-{votacion.pk}.csv"'
    writer = csv.writer(response)
    writer.writerow(["opcion", "votos", "porcentaje"])
    for fila in datos["opciones"]:
        writer.writerow([fila["nombre"], fila["votos"], fila["porcentaje"]])
    return response

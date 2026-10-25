from django.db.models import Count

from catalogo.models import Votacion
from votaciones.models import Voto


def puede_ver_resultados_publicos(votacion: Votacion) -> bool:
    visibilidad = votacion.visibilidad_resultados
    efectivo = votacion.estado_efectivo()
    if visibilidad == Votacion.Visibilidad.EN_VIVO:
        return efectivo != "borrador"
    if visibilidad == Votacion.Visibilidad.AL_CIERRE:
        return efectivo == "cerrada"
    return False


def agregar_resultados(votacion: Votacion) -> dict:
    total = Voto.objects.filter(votacion=votacion).count()
    filas = (
        votacion.opciones.annotate(total_votos=Count("votos"))
        .order_by("orden", "id")
        .values("id", "nombre", "descripcion", "total_votos")
    )
    opciones = []
    for fila in filas:
        votos = fila["total_votos"]
        porcentaje = round((votos * 100 / total), 1) if total else 0
        opciones.append(
            {
                "id": fila["id"],
                "nombre": fila["nombre"],
                "descripcion": fila["descripcion"],
                "votos": votos,
                "porcentaje": porcentaje,
            }
        )
    return {"total": total, "opciones": opciones}

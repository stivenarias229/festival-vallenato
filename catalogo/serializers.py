from django.utils import timezone
from django.utils.formats import date_format


def categoria_payload(categoria):
    return {
        "id": categoria.id,
        "nombre": categoria.nombre,
        "descripcion": categoria.descripcion,
        "icono": categoria.icono,
        "estado": categoria.estado,
        "edicion_id": categoria.edicion_id,
    }


def resumen_fecha(votacion) -> str:
    efectivo = votacion.estado_efectivo()
    inicio = date_format(timezone.localtime(votacion.fecha_inicio), "j \\d\\e F")
    fin = date_format(timezone.localtime(votacion.fecha_fin), "j \\d\\e F")
    if efectivo == "proxima":
        return f"Desde el {inicio}"
    if efectivo == "cerrada":
        return f"Cerró el {fin}"
    return f"Hasta el {fin}"


def votacion_payload(votacion, extra=None):
    data = {
        "id": votacion.id,
        "titulo": votacion.titulo,
        "fecha_inicio": votacion.fecha_inicio.isoformat(),
        "fecha_fin": votacion.fecha_fin.isoformat(),
        "estado": votacion.estado,
        "estado_efectivo": votacion.estado_efectivo(),
        "reglas": votacion.reglas,
        "visibilidad_resultados": votacion.visibilidad_resultados,
        "limite_votos_por_usuario": votacion.limite_votos_por_usuario,
        "categoria_id": votacion.categoria_id,
        "resumen_fecha": resumen_fecha(votacion),
    }
    if extra:
        data.update(extra)
    return data


def opcion_payload(opcion):
    return {
        "id": opcion.id,
        "nombre": opcion.nombre,
        "descripcion": opcion.descripcion,
        "imagen": opcion.imagen.url if opcion.imagen else None,
        "orden": opcion.orden,
        "votacion_id": opcion.votacion_id,
    }


def edicion_payload(edicion):
    return {
        "id": edicion.id,
        "nombre": edicion.nombre,
        "anio": edicion.anio,
        "estado": edicion.estado,
    }

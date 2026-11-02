"""Listados del panel: parámetros, orden en lista blanca, paginación y exportación."""

import csv
from io import BytesIO

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from openpyxl import Workbook

from auditoria.models import Auditoria
from auditoria.services import registrar_auditoria
from catalogo.models import Categoria, Votacion
from cuentas.models import Usuario

POR_PAGINA_PERMITIDOS = (10, 25, 50)
POR_PAGINA_DEFECTO = 10
Q_MAX = 100
TOPE_EXPORTACION = 10_000

USUARIOS_ORDEN = {
    "nombre": "nombre",
    "email": "email",
    "rol": "rol",
    "estado": "estado",
    "fecha_registro": "date_joined",
}
ACTIVIDAD_ORDEN = {
    "fecha_hora": "fecha_hora",
    "accion": "accion",
    "entidad_afectada": "entidad_afectada",
    "usuario": "usuario__nombre",
}
VOTACIONES_ORDEN = {
    "titulo": "titulo",
    "fecha_inicio": "fecha_inicio",
    "fecha_fin": "fecha_fin",
    "estado": "estado",
    "categoria": "categoria__nombre",
}
ESTADOS_VOTACION = {"borrador", "proxima", "abierta", "cerrada"}


def texto(request: HttpRequest, clave: str = "q") -> str:
    """Devuelve un texto de la query recortado, o cadena vacía."""
    return (request.GET.get(clave) or "").strip()[:Q_MAX]


def opcion(request: HttpRequest, clave: str, permitidos: set[str]) -> str:
    """Devuelve el valor solo si está en la lista blanca."""
    valor = (request.GET.get(clave) or "").strip()
    if valor in permitidos:
        return valor
    return ""


def por_pagina(request: HttpRequest) -> int:
    """Acepta 10, 25 o 50 filas. Cualquier otro valor vuelve a 10."""
    try:
        valor = int(request.GET.get("per_page", POR_PAGINA_DEFECTO))
    except (TypeError, ValueError):
        return POR_PAGINA_DEFECTO
    if valor not in POR_PAGINA_PERMITIDOS:
        return POR_PAGINA_DEFECTO
    return valor


def ordenar(
    queryset: QuerySet,
    request: HttpRequest,
    permitidos: dict[str, str],
    defecto: tuple[str, ...],
) -> tuple[QuerySet, str, str]:
    """Ordena solo con campos de la lista blanca. Un sort ajeno usa el orden por defecto."""
    sort = (request.GET.get("sort") or "").strip()
    if sort not in permitidos:
        sort = ""
    order = request.GET.get("order")
    if order not in {"asc", "desc"}:
        order = "desc"
    if not sort:
        return queryset.order_by(*defecto), "", "desc"
    prefijo = "" if order == "asc" else "-"
    desempate = "pk" if order == "asc" else "-pk"
    return queryset.order_by(f"{prefijo}{permitidos[sort]}", desempate), sort, order


def paginar(queryset: QuerySet, request: HttpRequest) -> tuple:
    """Corta el queryset con LIMIT/OFFSET y devuelve la página y el resumen."""
    tamano = por_pagina(request)
    paginator = Paginator(queryset, tamano)
    page = paginator.get_page(request.GET.get("page"))
    return page, {
        "number": page.number,
        "per_page": tamano,
        "count": paginator.count,
    }


def consulta_de(q: str, sort: str, order: str, filtros: dict[str, str]) -> dict:
    """Arma la consulta ya normalizada que vuelve a la página."""
    return {"q": q, "sort": sort, "order": order, "filtros": filtros}


def filtrar_estado_efectivo(queryset: QuerySet, estado: str, ahora=None) -> QuerySet:
    """Filtra por el estado visible, con la misma regla que Votacion.estado_efectivo."""
    if not estado:
        return queryset
    ahora = ahora or timezone.now()
    if estado == "borrador":
        return queryset.filter(estado=Votacion.Estado.BORRADOR)
    if estado == "proxima":
        return queryset.filter(estado=Votacion.Estado.ABIERTA, fecha_inicio__gt=ahora)
    if estado == "abierta":
        return queryset.filter(
            estado=Votacion.Estado.ABIERTA,
            fecha_inicio__lte=ahora,
            fecha_fin__gte=ahora,
        )
    if estado == "cerrada":
        return queryset.filter(
            Q(estado=Votacion.Estado.CERRADA) | Q(estado=Votacion.Estado.ABIERTA, fecha_fin__lt=ahora)
        )
    return queryset


def queryset_usuarios(request: HttpRequest) -> tuple[QuerySet, dict]:
    """Usuarios filtrados y ordenados, sin paginar."""
    q = texto(request)
    rol = opcion(request, "rol", {Usuario.Rol.VOTANTE, Usuario.Rol.ADMINISTRADOR})
    estado = opcion(request, "estado", {Usuario.Estado.ACTIVO, Usuario.Estado.BLOQUEADO})
    queryset = Usuario.objects.defer("password").annotate(votos_count=Count("votos"))
    if q:
        queryset = queryset.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
    if rol:
        queryset = queryset.filter(rol=rol)
    if estado:
        queryset = queryset.filter(estado=estado)
    queryset, sort, order = ordenar(queryset, request, USUARIOS_ORDEN, ("-date_joined", "-pk"))
    return queryset, consulta_de(q, sort, order, {"rol": rol, "estado": estado})


def queryset_actividad(request: HttpRequest) -> tuple[QuerySet, dict]:
    """Bitácora filtrada y ordenada, sin paginar."""
    q = texto(request)
    accion = texto(request, "accion")
    entidad = texto(request, "entidad_afectada")
    queryset = Auditoria.objects.select_related("usuario")
    if q:
        queryset = queryset.filter(
            Q(accion__icontains=q)
            | Q(entidad_afectada__icontains=q)
            | Q(detalle__icontains=q)
            | Q(usuario__nombre__icontains=q)
            | Q(usuario__email__icontains=q)
        )
    if accion:
        queryset = queryset.filter(accion__icontains=accion)
    if entidad:
        queryset = queryset.filter(entidad_afectada__icontains=entidad)
    queryset, sort, order = ordenar(queryset, request, ACTIVIDAD_ORDEN, ("-fecha_hora", "-pk"))
    return queryset, consulta_de(q, sort, order, {"accion": accion, "entidad_afectada": entidad})


def _categoria_id(request: HttpRequest) -> str:
    bruto = (request.GET.get("categoria") or "").strip()
    if not bruto.isdigit():
        return ""
    if not Categoria.objects.filter(pk=int(bruto)).exists():
        return ""
    return bruto


def queryset_votaciones(request: HttpRequest) -> tuple[QuerySet, dict]:
    """Votaciones filtradas y ordenadas, sin paginar."""
    q = texto(request)
    categoria = _categoria_id(request)
    estado = opcion(request, "estado", ESTADOS_VOTACION)
    queryset = Votacion.objects.select_related("categoria").annotate(opciones_count=Count("opciones"))
    if q:
        queryset = queryset.filter(Q(titulo__icontains=q) | Q(categoria__nombre__icontains=q))
    if categoria:
        queryset = queryset.filter(categoria_id=int(categoria))
    queryset = filtrar_estado_efectivo(queryset, estado)
    queryset, sort, order = ordenar(queryset, request, VOTACIONES_ORDEN, ("-fecha_inicio", "-pk"))
    return queryset, consulta_de(q, sort, order, {"categoria": categoria, "estado": estado})


def filas_usuarios(queryset: QuerySet):
    """Filas exportables de usuarios, sin contraseña."""
    for item in queryset:
        yield [
            item.nombre,
            item.email,
            item.rol,
            item.estado,
            item.date_joined.isoformat(),
            "sí" if item.votos_count > 0 else "no",
        ]


def filas_actividad(queryset: QuerySet):
    """Filas exportables de la bitácora."""
    for item in queryset:
        yield [
            item.fecha_hora.isoformat(),
            item.accion,
            item.entidad_afectada,
            item.usuario.nombre,
            item.usuario.email,
            item.detalle,
        ]


def filas_votaciones(queryset: QuerySet):
    """Filas exportables de votaciones."""
    for item in queryset:
        yield [
            item.titulo,
            item.categoria.nombre,
            item.fecha_inicio.isoformat(),
            item.fecha_fin.isoformat(),
            item.estado,
            item.estado_efectivo(),
            item.opciones_count,
        ]


def url_listado(request: HttpRequest, nombre_ruta: str) -> str:
    """URL del listado con la misma consulta, sin página ni formato."""
    params = request.GET.copy()
    params.pop("formato", None)
    params.pop("page", None)
    base = reverse(nombre_ruta)
    query = params.urlencode()
    return f"{base}?{query}" if query else base


def _respuesta_csv(nombre: str, columnas: list[str], filas: list) -> HttpResponse:
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{nombre}.csv"'
    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow(columnas)
    for fila in filas:
        writer.writerow(fila)
    return response


def _respuesta_xlsx(nombre: str, columnas: list[str], filas: list) -> HttpResponse:
    libro = Workbook()
    hoja = libro.active
    hoja.title = nombre
    hoja.append(columnas)
    for fila in filas:
        hoja.append(list(fila))
    buffer = BytesIO()
    libro.save(buffer)
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{nombre}.xlsx"'
    return response


def exportar_tabla(
    request: HttpRequest,
    queryset: QuerySet,
    *,
    columnas: list[str],
    filas,
    nombre: str,
    accion: str,
    entidad: str,
    detalle: str,
    volver: str,
) -> HttpResponse:
    """Genera CSV o XLSX del queryset completo, o redirige si el formato o el tamaño no sirven."""
    destino = url_listado(request, volver)
    formato = (request.GET.get("formato") or "").strip().lower()
    if formato not in {"csv", "xlsx"}:
        messages.error(request, "El formato de exportación no es válido.")
        return redirect(destino)
    if queryset.count() > TOPE_EXPORTACION:
        messages.error(
            request,
            "La exportación supera el límite de 10 000 filas. Ajusta los filtros.",
        )
        return redirect(destino)
    registrar_auditoria(request.user, accion, entidad, f"{detalle} ({formato}).")
    registros = list(filas(queryset))
    if formato == "csv":
        return _respuesta_csv(nombre, columnas, registros)
    return _respuesta_xlsx(nombre, columnas, registros)

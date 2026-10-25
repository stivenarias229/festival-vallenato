from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from inertia import render

from auditoria.models import Auditoria
from auditoria.services import registrar_auditoria
from catalogo.models import Categoria, Edicion, Opcion, Votacion
from catalogo.serializers import (
    categoria_payload,
    edicion_payload,
    opcion_payload,
    votacion_payload,
)
from cuentas.models import Usuario
from cuentas.permissions import requiere_administrador
from votaciones.models import Voto

from .forms import CategoriaForm, EdicionForm, OpcionForm, UsuarioAdminForm, VotacionForm
from .services import reordenar_opcion


def _pagina(queryset, request, por_pagina=10):
    paginator = Paginator(queryset, por_pagina)
    page = paginator.get_page(request.GET.get("page"))
    return page, {
        "number": page.number,
        "num_pages": paginator.num_pages,
        "count": paginator.count,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
        "next_page": page.next_page_number() if page.has_next() else None,
        "previous_page": page.previous_page_number() if page.has_previous() else None,
    }


@requiere_administrador
def inicio(request):
    ahora = timezone.now()
    abiertas = [
        votacion
        for votacion in Votacion.objects.select_related("categoria")
        if votacion.estado_efectivo(ahora) == "abierta"
    ]
    actividad = Auditoria.objects.select_related("usuario")[:5]
    return render(
        request,
        "Panel/Inicio",
        {
            "stats": {
                "votos": Voto.objects.count(),
                "votaciones_abiertas": len(abiertas),
                "usuarios": Usuario.objects.count(),
            },
            "actividad": [
                {
                    "id": item.id,
                    "accion": item.accion,
                    "detalle": item.detalle,
                    "fecha_hora": item.fecha_hora.isoformat(),
                    "usuario": item.usuario.nombre,
                }
                for item in actividad
            ],
        },
    )


@requiere_administrador
def categorias(request):
    if request.method == "POST":
        accion = request.POST.get("accion")
        if accion == "guardar_edicion":
            edicion = None
            if request.POST.get("id"):
                edicion = get_object_or_404(Edicion, pk=request.POST.get("id"))
            form = EdicionForm(request.POST, instance=edicion)
            if form.is_valid():
                guardada = form.save()
                registrar_auditoria(
                    request.user,
                    "editar_edicion" if edicion else "crear_edicion",
                    "edicion",
                    f"{guardada.nombre} {guardada.anio}",
                )
                messages.success(request, "Edición guardada.")
            else:
                messages.error(request, "Revisa los datos de la edición.")
            return redirect("panel_categorias")
        if accion == "guardar_categoria":
            categoria = None
            if request.POST.get("id"):
                categoria = get_object_or_404(Categoria, pk=request.POST.get("id"))
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                guardada = form.save()
                registrar_auditoria(
                    request.user,
                    "editar_categoria" if categoria else "crear_categoria",
                    "categoria",
                    guardada.nombre,
                )
                messages.success(request, "Categoría guardada.")
            else:
                messages.error(request, "Revisa los datos de la categoría.")
            return redirect("panel_categorias")
        if accion == "toggle_categoria":
            categoria = get_object_or_404(Categoria, pk=request.POST.get("id"))
            if categoria.estado == Categoria.Estado.ACTIVA and categoria.votaciones.filter(
                estado=Votacion.Estado.ABIERTA
            ).exists():
                messages.error(
                    request,
                    "No puedes desactivar una categoría con votaciones abiertas.",
                )
                return redirect("panel_categorias")
            categoria.estado = (
                Categoria.Estado.INACTIVA
                if categoria.estado == Categoria.Estado.ACTIVA
                else Categoria.Estado.ACTIVA
            )
            categoria.save(update_fields=["estado"])
            registrar_auditoria(
                request.user,
                "desactivar_categoria" if categoria.estado == Categoria.Estado.INACTIVA else "activar_categoria",
                "categoria",
                categoria.nombre,
            )
            messages.success(request, "Estado de la categoría actualizado.")
            return redirect("panel_categorias")
    return render(
        request,
        "Panel/Categorias",
        {
            "ediciones": [edicion_payload(item) for item in Edicion.objects.order_by("-anio")],
            "categorias": [
                categoria_payload(item)
                for item in Categoria.objects.select_related("edicion").all()
            ],
        },
    )


@requiere_administrador
def votaciones(request):
    if request.method == "POST":
        accion = request.POST.get("accion")
        if accion == "guardar":
            votacion = None
            if request.POST.get("id"):
                votacion = get_object_or_404(Votacion, pk=request.POST.get("id"))
            form = VotacionForm(request.POST, instance=votacion)
            if form.is_valid():
                guardada = form.save()
                registrar_auditoria(
                    request.user,
                    "editar_votacion" if votacion else "crear_votacion",
                    "votacion",
                    guardada.titulo,
                )
                messages.success(request, "Votación guardada.")
            else:
                messages.error(request, form.non_field_errors().as_text() or "Revisa los datos.")
            return redirect("panel_votaciones")
        if accion in {"abrir", "cerrar"}:
            votacion = get_object_or_404(Votacion, pk=request.POST.get("id"))
            if accion == "abrir" and not votacion.opciones.exists():
                messages.error(request, "No puedes abrir una votación sin opciones.")
                return redirect("panel_votaciones")
            votacion.estado = (
                Votacion.Estado.ABIERTA if accion == "abrir" else Votacion.Estado.CERRADA
            )
            votacion.save(update_fields=["estado"])
            registrar_auditoria(request.user, f"{accion}_votacion", "votacion", votacion.titulo)
            messages.success(
                request,
                "Votación abierta." if accion == "abrir" else "Votación cerrada.",
            )
            return redirect("panel_votaciones")
    return render(
        request,
        "Panel/Votaciones",
        {
            "categorias": [
                categoria_payload(item)
                for item in Categoria.objects.filter(estado=Categoria.Estado.ACTIVA)
            ],
            "votaciones": [
                votacion_payload(
                    item,
                    extra={"opciones_count": item.opciones.count()},
                )
                for item in Votacion.objects.select_related("categoria").prefetch_related("opciones")
            ],
        },
    )


@requiere_administrador
def opciones(request, votacion_id):
    votacion = get_object_or_404(Votacion.objects.select_related("categoria"), pk=votacion_id)
    if request.method == "POST":
        accion = request.POST.get("accion")
        if accion == "guardar":
            opcion = None
            if request.POST.get("id"):
                opcion = get_object_or_404(Opcion, pk=request.POST.get("id"), votacion=votacion)
            form = OpcionForm(request.POST, request.FILES, instance=opcion)
            if form.is_valid():
                guardada = form.save(commit=False)
                guardada.votacion = votacion
                guardada.save()
                registrar_auditoria(
                    request.user,
                    "editar_opcion" if opcion else "crear_opcion",
                    "opcion",
                    f"{guardada.nombre} en {votacion.titulo}",
                )
                messages.success(request, "Opción guardada.")
            else:
                messages.error(request, "Revisa los datos de la opción.")
            return redirect("panel_opciones", votacion_id=votacion.pk)
        if accion in {"subir", "bajar"}:
            opcion = get_object_or_404(Opcion, pk=request.POST.get("id"), votacion=votacion)
            if reordenar_opcion(votacion, opcion, accion):
                registrar_auditoria(
                    request.user,
                    "ordenar_opcion",
                    "opcion",
                    f"{opcion.nombre} en {votacion.titulo}",
                )
                messages.success(request, "Orden de la opción actualizado.")
            else:
                messages.info(request, "Esa opción ya está al extremo de la lista.")
            return redirect("panel_opciones", votacion_id=votacion.pk)
    return render(
        request,
        "Panel/Opciones",
        {
            "votacion": votacion_payload(votacion),
            "opciones": [opcion_payload(item) for item in votacion.opciones.all()],
            "votaciones": [
                votacion_payload(item) for item in Votacion.objects.select_related("categoria")
            ],
        },
    )


@requiere_administrador
def usuarios(request):
    if request.method == "POST":
        objetivo = get_object_or_404(Usuario, pk=request.POST.get("id"))
        if objetivo.pk == request.user.pk:
            messages.error(request, "No puedes bloquearte ni cambiarte el rol a ti mismo.")
            return redirect("panel_usuarios")
        form = UsuarioAdminForm(request.POST)
        if form.is_valid():
            objetivo.rol = form.cleaned_data["rol"]
            objetivo.estado = form.cleaned_data["estado"]
            objetivo.save(update_fields=["rol", "estado"])
            registrar_auditoria(
                request.user,
                "gestionar_usuario",
                "usuario",
                f"{objetivo.email} → {objetivo.rol}/{objetivo.estado}",
            )
            messages.success(request, "Usuario actualizado.")
        return redirect("panel_usuarios")

    filtro = request.GET.get("filtro", "todos")
    q = request.GET.get("q", "").strip()
    queryset = Usuario.objects.annotate(votos_count=Count("votos")).order_by("-date_joined")
    if q:
        queryset = queryset.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
    if filtro == "votante":
        queryset = queryset.filter(rol=Usuario.Rol.VOTANTE)
    elif filtro == "administrador":
        queryset = queryset.filter(rol=Usuario.Rol.ADMINISTRADOR)
    elif filtro == "bloqueados":
        queryset = queryset.filter(estado=Usuario.Estado.BLOQUEADO)
    page, paginacion = _pagina(queryset, request, 8)
    return render(
        request,
        "Panel/Usuarios",
        {
            "usuarios": [
                {
                    "id": item.id,
                    "nombre": item.nombre,
                    "email": item.email,
                    "rol": item.rol,
                    "estado": item.estado,
                    "fecha_registro": item.date_joined.isoformat(),
                    "tiene_votos": item.votos_count > 0,
                }
                for item in page
            ],
            "filtro": filtro,
            "q": q,
            "paginacion": paginacion,
        },
    )


@requiere_administrador
def actividad(request):
    page, paginacion = _pagina(
        Auditoria.objects.select_related("usuario"),
        request,
        15,
    )
    return render(
        request,
        "Panel/Actividad",
        {
            "actividad": [
                {
                    "id": item.id,
                    "accion": item.accion,
                    "entidad_afectada": item.entidad_afectada,
                    "detalle": item.detalle,
                    "fecha_hora": item.fecha_hora.isoformat(),
                    "usuario": item.usuario.nombre,
                    "email": item.usuario.email,
                }
                for item in page
            ],
            "paginacion": paginacion,
        },
    )

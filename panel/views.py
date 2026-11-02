from django.contrib import messages
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
from .listados import (
    exportar_tabla,
    filas_actividad,
    filas_usuarios,
    filas_votaciones,
    paginar,
    queryset_actividad,
    queryset_usuarios,
    queryset_votaciones,
)
from .services import reordenar_opcion


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
            return redirect(request.get_full_path())
        if accion in {"abrir", "cerrar"}:
            votacion = get_object_or_404(Votacion, pk=request.POST.get("id"))
            if accion == "abrir" and not votacion.opciones.exists():
                messages.error(request, "No puedes abrir una votación sin opciones.")
                return redirect(request.get_full_path())
            votacion.estado = (
                Votacion.Estado.ABIERTA if accion == "abrir" else Votacion.Estado.CERRADA
            )
            votacion.save(update_fields=["estado"])
            registrar_auditoria(request.user, f"{accion}_votacion", "votacion", votacion.titulo)
            messages.success(
                request,
                "Votación abierta." if accion == "abrir" else "Votación cerrada.",
            )
            return redirect(request.get_full_path())
    queryset, consulta = queryset_votaciones(request)
    page, paginacion = paginar(queryset, request)
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
                    extra={
                        "opciones_count": item.opciones_count,
                        "categoria_nombre": item.categoria.nombre,
                    },
                )
                for item in page
            ],
            "paginacion": paginacion,
            "consulta": consulta,
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
            return redirect(request.get_full_path())
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
        return redirect(request.get_full_path())

    queryset, consulta = queryset_usuarios(request)
    page, paginacion = paginar(queryset, request)
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
            "paginacion": paginacion,
            "consulta": consulta,
        },
    )


@requiere_administrador
def actividad(request):
    queryset, consulta = queryset_actividad(request)
    page, paginacion = paginar(queryset, request)
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
            "consulta": consulta,
        },
    )


@requiere_administrador
def exportar_usuarios(request):
    queryset, _consulta = queryset_usuarios(request)
    return exportar_tabla(
        request,
        queryset,
        columnas=["nombre", "correo", "rol", "estado", "fecha de registro", "tiene votos"],
        filas=filas_usuarios,
        nombre="usuarios",
        accion="exportar_usuarios",
        entidad="usuario",
        detalle="Exportó el listado de usuarios",
        volver="panel_usuarios",
    )


@requiere_administrador
def exportar_actividad(request):
    queryset, _consulta = queryset_actividad(request)
    return exportar_tabla(
        request,
        queryset,
        columnas=["fecha", "acción", "entidad", "quién", "correo", "detalle"],
        filas=filas_actividad,
        nombre="actividad",
        accion="exportar_actividad",
        entidad="auditoria",
        detalle="Exportó la bitácora",
        volver="panel_actividad",
    )


@requiere_administrador
def exportar_votaciones(request):
    queryset, _consulta = queryset_votaciones(request)
    return exportar_tabla(
        request,
        queryset,
        columnas=[
            "título",
            "categoría",
            "inicio",
            "cierre",
            "estado guardado",
            "estado visible",
            "cantidad de opciones",
        ],
        filas=filas_votaciones,
        nombre="votaciones",
        accion="exportar_votaciones",
        entidad="votacion",
        detalle="Exportó el listado de votaciones",
        volver="panel_votaciones",
    )

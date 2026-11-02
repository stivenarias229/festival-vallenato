import csv
from datetime import timedelta
from io import BytesIO

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone
from openpyxl import load_workbook

from auditoria.models import Auditoria
from auditoria.services import registrar_auditoria
from catalogo.models import Categoria, Votacion
from cuentas.models import Usuario
def _props(client, nombre, **params):
    response = client.get(reverse(nombre), params, HTTP_X_INERTIA="true")
    assert response.status_code == 200
    return response.json()["props"]


def _filas_csv(response):
    contenido = response.content.decode("utf-8-sig")
    return list(csv.reader(contenido.splitlines()))


def _hoja(response):
    libro = load_workbook(BytesIO(response.content))
    return libro.active


@pytest.mark.django_db
def test_pagina_2_devuelve_el_corte_y_el_total(client, usuario_admin):
    client.force_login(usuario_admin)
    ahora = timezone.now()
    usuario_admin.date_joined = ahora - timedelta(days=1)
    usuario_admin.save(update_fields=["date_joined"])
    for indice in range(12):
        usuario = Usuario.objects.create_user(
            email=f"u{indice}@correo.com",
            password="ClaveSegura2027!",
            nombre=f"Persona {indice:02d}",
        )
        usuario.date_joined = ahora - timedelta(minutes=indice)
        usuario.save(update_fields=["date_joined"])

    props = _props(client, "panel_usuarios", page=2, per_page=10)
    assert props["paginacion"] == {"number": 2, "per_page": 10, "count": 13}
    assert len(props["usuarios"]) == 3
    assert "password" not in str(props)


@pytest.mark.django_db
def test_pagina_invalida_cae_en_un_extremo(client, usuario_admin):
    client.force_login(usuario_admin)
    props = _props(client, "panel_usuarios", page="abc")
    assert props["paginacion"]["number"] == 1
    props = _props(client, "panel_usuarios", page=999)
    assert props["paginacion"]["number"] == 1


@pytest.mark.django_db
def test_per_page_ajeno_vuelve_a_10(client, usuario_admin):
    client.force_login(usuario_admin)
    props = _props(client, "panel_usuarios", per_page=9999)
    assert props["paginacion"]["per_page"] == 10


@pytest.mark.django_db
def test_sort_desconocido_no_cambia_el_orden_ni_llega_al_order_by(client, usuario_admin):
    client.force_login(usuario_admin)
    ahora = timezone.now()
    reciente = Usuario.objects.create_user(
        email="reciente@correo.com",
        password="ClaveSegura2027!",
        nombre="Reciente",
    )
    reciente.date_joined = ahora
    reciente.save(update_fields=["date_joined"])
    usuario_admin.date_joined = ahora - timedelta(days=2)
    usuario_admin.save(update_fields=["date_joined"])

    with CaptureQueriesContext(connection) as consultas:
        props = _props(client, "panel_usuarios", sort="password", order="asc")
    assert props["consulta"]["sort"] == ""
    assert props["usuarios"][0]["nombre"] == "Reciente"
    ordenes = [item["sql"].lower().split("order by", 1)[1] for item in consultas.captured_queries if "order by" in item["sql"].lower()]
    assert ordenes
    assert all("password" not in orden for orden in ordenes)


@pytest.mark.django_db
def test_busqueda_y_filtros_de_usuarios(client, usuario_admin, usuario_votante):
    client.force_login(usuario_admin)
    usuario_votante.estado = Usuario.Estado.BLOQUEADO
    usuario_votante.save(update_fields=["estado"])

    por_nombre = _props(client, "panel_usuarios", q="votante demo")
    assert [item["email"] for item in por_nombre["usuarios"]] == ["votante@correo.com"]

    por_rol = _props(client, "panel_usuarios", rol="administrador")
    assert [item["email"] for item in por_rol["usuarios"]] == ["admin@festival.example"]

    invalido = _props(client, "panel_usuarios", rol="superuser")
    assert invalido["consulta"]["filtros"]["rol"] == ""
    assert invalido["paginacion"]["count"] == 2

    bloqueados = _props(client, "panel_usuarios", estado="bloqueado")
    assert [item["email"] for item in bloqueados["usuarios"]] == ["votante@correo.com"]

    largo = _props(client, "panel_usuarios", q="a" * 150)
    assert largo["consulta"]["q"] == "a" * 100


@pytest.mark.django_db
def test_orden_valido_de_usuarios(client, usuario_admin, usuario_votante):
    client.force_login(usuario_admin)
    props = _props(client, "panel_usuarios", sort="nombre", order="asc")
    assert props["consulta"]["sort"] == "nombre"
    assert props["consulta"]["order"] == "asc"
    assert [item["nombre"] for item in props["usuarios"]] == ["Admin Festival", "Votante Demo"]


@pytest.mark.django_db
def test_post_de_usuario_conserva_la_consulta(client, usuario_admin, usuario_votante):
    client.force_login(usuario_admin)
    response = client.post(
        reverse("panel_usuarios") + "?page=2&q=ana&rol=votante",
        {"id": usuario_votante.pk, "rol": "administrador", "estado": "activo"},
    )
    assert response.status_code == 302
    assert "page=2" in response.url
    assert "q=ana" in response.url
    assert "rol=votante" in response.url


@pytest.mark.django_db
def test_actividad_pagina_busca_filtra_y_ordena(client, usuario_admin, usuario_votante):
    client.force_login(usuario_admin)
    for indice in range(11):
        registrar_auditoria(usuario_admin, f"accion-{indice:02d}", "categoria", f"detalle {indice}")
    registrar_auditoria(usuario_votante, "cerrar_votacion", "votacion", "Cerró la final")

    props = _props(client, "panel_actividad", page=2, per_page=10)
    assert props["paginacion"]["count"] == 12
    assert len(props["actividad"]) == 2
    assert "fecha_hora" in props["actividad"][0]

    encontrada = _props(client, "panel_actividad", q="final")
    assert [item["accion"] for item in encontrada["actividad"]] == ["cerrar_votacion"]

    por_correo = _props(client, "panel_actividad", q="votante@correo.com")
    assert [item["email"] for item in por_correo["actividad"]] == ["votante@correo.com"]

    filtrada = _props(client, "panel_actividad", accion="cerrar")
    assert filtrada["consulta"]["filtros"]["accion"] == "cerrar"
    assert [item["accion"] for item in filtrada["actividad"]] == ["cerrar_votacion"]

    larga = _props(client, "panel_actividad", entidad_afectada="x" * 150)
    assert larga["consulta"]["filtros"]["entidad_afectada"] == "x" * 100

    ordenada = _props(client, "panel_actividad", sort="usuario", order="asc")
    assert ordenada["actividad"][0]["usuario"] == "Admin Festival"
    desconocido = _props(client, "panel_actividad", sort="detalle")
    assert desconocido["consulta"]["sort"] == ""


@pytest.mark.django_db
def test_votaciones_filtran_por_estado_visible_y_categoria(client, usuario_admin, catalogo_abierto):
    client.force_login(usuario_admin)
    ahora = timezone.now()
    categoria = catalogo_abierto["categoria"]
    otra = Categoria.objects.create(
        edicion=catalogo_abierto["edicion"],
        nombre="Rey vallenato",
        descripcion="",
        estado=Categoria.Estado.INACTIVA,
    )
    Votacion.objects.create(
        categoria=categoria,
        titulo="Borrador secreto",
        fecha_inicio=ahora,
        fecha_fin=ahora + timedelta(days=1),
        estado=Votacion.Estado.BORRADOR,
    )
    Votacion.objects.create(
        categoria=categoria,
        titulo="Todavía no",
        fecha_inicio=ahora + timedelta(days=3),
        fecha_fin=ahora + timedelta(days=4),
        estado=Votacion.Estado.ABIERTA,
    )
    Votacion.objects.create(
        categoria=categoria,
        titulo="Ya cerrada",
        fecha_inicio=ahora - timedelta(days=4),
        fecha_fin=ahora - timedelta(days=1),
        estado=Votacion.Estado.ABIERTA,
    )
    Votacion.objects.create(
        categoria=otra,
        titulo="Cierre manual",
        fecha_inicio=ahora - timedelta(days=1),
        fecha_fin=ahora + timedelta(days=1),
        estado=Votacion.Estado.CERRADA,
    )

    abiertas = _props(client, "panel_votaciones", estado="abierta")
    assert [item["titulo"] for item in abiertas["votaciones"]] == ["Canción favorita"]

    proximas = _props(client, "panel_votaciones", estado="proxima")
    assert [item["titulo"] for item in proximas["votaciones"]] == ["Todavía no"]

    cerradas = _props(client, "panel_votaciones", estado="cerrada")
    assert {item["titulo"] for item in cerradas["votaciones"]} == {"Ya cerrada", "Cierre manual"}

    borradores = _props(client, "panel_votaciones", estado="borrador")
    assert [item["titulo"] for item in borradores["votaciones"]] == ["Borrador secreto"]

    invalido = _props(client, "panel_votaciones", estado="inventado")
    assert invalido["consulta"]["filtros"]["estado"] == ""
    assert invalido["paginacion"]["count"] == 5

    de_otra = _props(client, "panel_votaciones", categoria=otra.pk)
    assert [item["titulo"] for item in de_otra["votaciones"]] == ["Cierre manual"]
    assert de_otra["votaciones"][0]["opciones_count"] == 0
    assert de_otra["votaciones"][0]["categoria_nombre"] == "Rey vallenato"

    fantasma = _props(client, "panel_votaciones", categoria=99999)
    assert fantasma["consulta"]["filtros"]["categoria"] == ""
    assert fantasma["paginacion"]["count"] == 5

    nombres_formulario = {item["nombre"] for item in _props(client, "panel_votaciones")["categorias"]}
    assert "Rey vallenato" not in nombres_formulario

    orden = _props(client, "panel_votaciones", sort="titulo", order="asc")
    assert [item["titulo"] for item in orden["votaciones"]][0] == "Borrador secreto"


@pytest.mark.django_db
def test_post_de_votacion_conserva_la_consulta(client, usuario_admin, catalogo_abierto):
    client.force_login(usuario_admin)
    response = client.post(
        reverse("panel_votaciones") + "?page=2&q=cancion",
        {"accion": "cerrar", "id": catalogo_abierto["votacion"].pk},
    )
    assert response.status_code == 302
    assert "page=2" in response.url
    assert "q=cancion" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "nombre",
    ["panel_usuarios_exportar", "panel_actividad_exportar", "panel_votaciones_exportar"],
)
def test_anonimo_no_exporta(client, nombre):
    response = client.get(reverse(nombre), {"formato": "csv"})
    assert response.status_code == 302
    assert reverse("ingresar") in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "nombre",
    ["panel_usuarios_exportar", "panel_actividad_exportar", "panel_votaciones_exportar"],
)
def test_votante_no_exporta(client, usuario_votante, nombre):
    client.force_login(usuario_votante)
    response = client.get(reverse(nombre), {"formato": "csv"})
    assert response.status_code == 403


@pytest.mark.django_db
def test_csv_de_usuarios_respeta_filtro_e_ignora_la_pagina(client, usuario_admin):
    client.force_login(usuario_admin)
    for indice in range(12):
        Usuario.objects.create_user(
            email=f"lista{indice}@correo.com",
            password="ClaveSegura2027!",
            nombre=f"Lista {indice}",
        )
    response = client.get(
        reverse("panel_usuarios_exportar"),
        {"formato": "csv", "rol": "votante", "page": 2, "per_page": 10, "sort": "password"},
    )
    assert response.status_code == 200
    assert "text/csv" in response["Content-Type"]
    assert 'filename="usuarios.csv"' in response["Content-Disposition"]
    filas = _filas_csv(response)
    assert filas[0] == ["nombre", "correo", "rol", "estado", "fecha de registro", "tiene votos"]
    assert len(filas) == 13
    assert "admin@festival.example" not in response.content.decode()
    assert "ClaveSegura2027" not in response.content.decode()
    assert Auditoria.objects.filter(accion="exportar_usuarios").exists()


@pytest.mark.django_db
def test_xlsx_de_usuarios_respeta_el_filtro(client, usuario_admin, usuario_votante):
    client.force_login(usuario_admin)
    response = client.get(
        reverse("panel_usuarios_exportar"),
        {"formato": "xlsx", "estado": "activo", "page": 2, "per_page": 1},
    )
    assert response.status_code == 200
    assert "spreadsheetml" in response["Content-Type"]
    hoja = _hoja(response)
    correos = [fila[1] for fila in hoja.iter_rows(min_row=2, values_only=True)]
    assert "admin@festival.example" in correos
    assert "votante@correo.com" in correos
    assert hoja.max_row == 3


@pytest.mark.django_db
def test_exportar_rechaza_formato_invalido_y_el_tope(client, usuario_admin, monkeypatch):
    client.force_login(usuario_admin)
    invalido = client.get(reverse("panel_usuarios_exportar"), {"formato": "pdf"})
    assert invalido.status_code == 302
    assert not Auditoria.objects.filter(accion="exportar_usuarios").exists()

    monkeypatch.setattr("panel.listados.TOPE_EXPORTACION", 0)
    exceso = client.get(reverse("panel_usuarios_exportar"), {"formato": "csv"})
    assert exceso.status_code == 302
    assert "text/csv" not in exceso.get("Content-Type", "")
    assert not Auditoria.objects.filter(accion="exportar_usuarios").exists()


@pytest.mark.django_db
def test_exportar_actividad_y_votaciones(client, usuario_admin, catalogo_abierto):
    client.force_login(usuario_admin)
    registrar_auditoria(usuario_admin, "crear_categoria", "categoria", "Acordeón")
    csv_actividad = client.get(reverse("panel_actividad_exportar"), {"formato": "csv", "q": "Acordeón"})
    filas = _filas_csv(csv_actividad)
    assert filas[0][0] == "fecha"
    assert filas[1][1] == "crear_categoria"
    assert len(filas) == 2

    xlsx = client.get(reverse("panel_votaciones_exportar"), {"formato": "xlsx", "q": "Canción"})
    hoja = _hoja(xlsx)
    assert hoja.cell(1, 1).value == "título"
    assert hoja.cell(2, 1).value == "Canción favorita"
    assert hoja.cell(2, 7).value == 2
    assert Auditoria.objects.filter(accion="exportar_votaciones").exists()

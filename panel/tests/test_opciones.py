import json

import pytest
from django.urls import reverse

from catalogo.models import Opcion


def _json_post(client, url, payload):
    return client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_X_INERTIA="true",
    )


@pytest.mark.django_db
def test_subir_reordena_aunque_compartan_orden(client, usuario_admin, catalogo_abierto):
    votacion = catalogo_abierto["votacion"]
    primera = catalogo_abierto["opcion"]
    segunda = votacion.opciones.exclude(pk=primera.pk).get()
    votacion.opciones.update(orden=0)
    primera.refresh_from_db()
    segunda.refresh_from_db()
    client.force_login(usuario_admin)

    response = _json_post(
        client,
        reverse("panel_opciones", args=[votacion.pk]),
        {"accion": "subir", "id": segunda.pk},
    )

    assert response.status_code == 302
    nombres = list(votacion.opciones.order_by("orden", "id").values_list("nombre", flat=True))
    assert nombres[0] == segunda.nombre
    assert list(votacion.opciones.order_by("orden", "id").values_list("orden", flat=True)) == [1, 2]


@pytest.mark.django_db
def test_bajar_intercambia_con_la_siguiente(client, usuario_admin, catalogo_abierto):
    votacion = catalogo_abierto["votacion"]
    primera = catalogo_abierto["opcion"]
    client.force_login(usuario_admin)

    _json_post(
        client,
        reverse("panel_opciones", args=[votacion.pk]),
        {"accion": "bajar", "id": primera.pk},
    )

    nombres = list(votacion.opciones.order_by("orden", "id").values_list("nombre", flat=True))
    assert nombres[0] != primera.nombre


@pytest.mark.django_db
def test_editar_opcion_actualiza_nombre(client, usuario_admin, catalogo_abierto):
    votacion = catalogo_abierto["votacion"]
    opcion = catalogo_abierto["opcion"]
    client.force_login(usuario_admin)

    response = _json_post(
        client,
        reverse("panel_opciones", args=[votacion.pk]),
        {
            "accion": "guardar",
            "id": opcion.pk,
            "nombre": "Luis Mejía",
            "descripcion": "Artista de vallenato",
            "orden": 1,
        },
    )

    assert response.status_code == 302
    opcion.refresh_from_db()
    assert opcion.nombre == "Luis Mejía"


@pytest.mark.django_db
def test_bajar_funciona_con_ordenes_duplicados(client, usuario_admin, catalogo_abierto):
    votacion = catalogo_abierto["votacion"]
    primera, segunda = list(votacion.opciones.order_by("orden", "id"))
    votacion.opciones.update(orden=1)
    client.force_login(usuario_admin)

    _json_post(
        client,
        reverse("panel_opciones", args=[votacion.pk]),
        {"accion": "bajar", "id": primera.pk},
    )

    nombres = list(votacion.opciones.order_by("orden", "id").values_list("nombre", flat=True))
    assert nombres[0] == segunda.nombre
    assert list(votacion.opciones.order_by("orden", "id").values_list("orden", flat=True)) == [1, 2]


@pytest.mark.django_db
def test_subir_la_primera_no_cambia_el_orden(client, usuario_admin, catalogo_abierto):
    votacion = catalogo_abierto["votacion"]
    primera = catalogo_abierto["opcion"]
    client.force_login(usuario_admin)
    antes = list(votacion.opciones.order_by("orden", "id").values_list("pk", flat=True))

    _json_post(
        client,
        reverse("panel_opciones", args=[votacion.pk]),
        {"accion": "subir", "id": primera.pk},
    )

    despues = list(votacion.opciones.order_by("orden", "id").values_list("pk", flat=True))
    assert despues == antes

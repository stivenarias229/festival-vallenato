import pytest
from django.urls import reverse

from catalogo.models import Votacion
from votaciones.models import Voto


def _get(client, votacion, user=None):
    if user:
        client.force_login(user)
    return client.get(
        reverse("resultados_publicos", args=[votacion.pk]),
        HTTP_X_INERTIA="true",
    )


@pytest.mark.django_db
def test_internos_no_son_publicos(client, catalogo_abierto, usuario_votante, usuario_admin):
    votacion = catalogo_abierto["votacion"]
    votacion.visibilidad_resultados = Votacion.Visibilidad.INTERNOS
    votacion.save(update_fields=["visibilidad_resultados"])
    assert _get(client, votacion).json()["props"]["disponible"] is False
    client.logout()
    assert _get(client, votacion, usuario_votante).json()["props"]["disponible"] is False
    client.logout()
    client.force_login(usuario_admin)
    admin = client.get(reverse("panel_resultados"), HTTP_X_INERTIA="true")
    payload = str(admin.json()["props"])
    assert "password" not in payload
    assert "total" in admin.json()["props"]["resultados"]
    assert "opciones" in admin.json()["props"]["resultados"]


@pytest.mark.django_db
def test_en_vivo_y_al_cierre(client, catalogo_abierto, usuario_votante):
    votacion = catalogo_abierto["votacion"]
    votacion.visibilidad_resultados = Votacion.Visibilidad.EN_VIVO
    votacion.save(update_fields=["visibilidad_resultados"])
    assert _get(client, votacion).json()["props"]["disponible"] is True
    votacion.visibilidad_resultados = Votacion.Visibilidad.AL_CIERRE
    votacion.estado = Votacion.Estado.ABIERTA
    votacion.save(update_fields=["visibilidad_resultados", "estado"])
    assert _get(client, votacion).json()["props"]["disponible"] is False
    votacion.estado = Votacion.Estado.CERRADA
    votacion.save(update_fields=["estado"])
    props = _get(client, votacion).json()["props"]
    assert props["disponible"] is True
    assert "voto_id" not in str(props)


@pytest.mark.django_db
def test_csv_solo_agregados(client, usuario_admin, catalogo_abierto, usuario_votante):
    Voto.objects.create(
        usuario=usuario_votante,
        opcion=catalogo_abierto["opcion"],
        votacion=catalogo_abierto["votacion"],
    )
    client.force_login(usuario_admin)
    response = client.get(
        reverse("panel_resultados_csv", args=[catalogo_abierto["votacion"].pk])
    )
    contenido = response.content.decode()
    assert "opcion,votos,porcentaje" in contenido
    assert "votante@correo.com" not in contenido
    assert str(usuario_votante.pk) not in contenido

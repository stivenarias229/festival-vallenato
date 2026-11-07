import pytest
from django.urls import reverse

from votaciones.models import Voto


@pytest.mark.django_db
def test_confirmar_pide_login(client, catalogo_abierto):
    url = reverse("voto_confirmar", args=[catalogo_abierto["votacion"].pk])
    response = client.get(f"{url}?opcion={catalogo_abierto['opcion'].pk}")
    assert response.status_code == 302
    assert reverse("ingresar") in response.url


@pytest.mark.django_db
def test_post_votar_registra(client, usuario_votante, catalogo_abierto):
    client.force_login(usuario_votante)
    response = client.post(
        reverse("votar", args=[catalogo_abierto["votacion"].pk]),
        {"opcion_id": catalogo_abierto["opcion"].pk, "confirmado": "1"},
    )
    assert response.status_code == 302
    assert Voto.objects.filter(usuario=usuario_votante).count() == 1


@pytest.mark.django_db
def test_sin_confirmacion_no_registra(client, usuario_votante, catalogo_abierto):
    client.force_login(usuario_votante)
    client.post(
        reverse("votar", args=[catalogo_abierto["votacion"].pk]),
        {"opcion_id": catalogo_abierto["opcion"].pk},
    )
    assert Voto.objects.filter(usuario=usuario_votante).count() == 0


@pytest.mark.django_db
def test_mis_votos_pide_login(client):
    response = client.get(reverse("mis_votos"))
    assert response.status_code == 302
    assert reverse("ingresar") in response.url


@pytest.mark.django_db
def test_mis_votos_lista_participacion(client, usuario_votante, catalogo_abierto):
    client.force_login(usuario_votante)
    vacio = client.get(reverse("mis_votos"), HTTP_X_INERTIA="true")
    assert vacio.json()["component"] == "Votaciones/MisVotos"
    assert vacio.json()["props"]["votos"] == []

    Voto.objects.create(
        usuario=usuario_votante,
        votacion=catalogo_abierto["votacion"],
        opcion=catalogo_abierto["opcion"],
    )
    response = client.get(reverse("mis_votos"), HTTP_X_INERTIA="true")
    votos = response.json()["props"]["votos"]
    assert len(votos) == 1
    assert votos[0]["categoria"]["nombre"] == "Acordeón"
    assert votos[0]["votacion"]["titulo"] == "Canción favorita"
    assert votos[0]["opcion"]["nombre"] == "Opción A"

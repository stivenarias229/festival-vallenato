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

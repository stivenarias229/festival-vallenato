import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_inicio_y_categorias_props(client, catalogo_abierto):
    inicio = client.get(reverse("inicio"), HTTP_X_INERTIA="true")
    assert inicio.json()["component"] == "Publico/Inicio"
    categorias = client.get(reverse("categorias"), HTTP_X_INERTIA="true")
    assert categorias.json()["component"] == "Publico/Categorias"
    assert categorias.json()["props"]["categorias"][0]["nombre"] == "Acordeón"


@pytest.mark.django_db
def test_inicio_comparte_si_hay_sesion(client, usuario_votante):
    anonimo = client.get(reverse("inicio"), HTTP_X_INERTIA="true")
    assert anonimo.json()["props"]["auth"]["user"] is None

    client.force_login(usuario_votante)
    autenticado = client.get(reverse("inicio"), HTTP_X_INERTIA="true")
    assert autenticado.json()["props"]["auth"]["user"]["id"] == usuario_votante.pk


@pytest.mark.django_db
def test_votaciones_filtradas_por_categoria(client, catalogo_abierto):
    response = client.get(
        reverse("categoria_votaciones", args=[catalogo_abierto["categoria"].pk]),
        HTTP_X_INERTIA="true",
    )
    titulos = [item["titulo"] for item in response.json()["props"]["votaciones"]]
    assert "Canción favorita" in titulos

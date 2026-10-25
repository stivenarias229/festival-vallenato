import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_anonimo_va_a_login(client):
    response = client.get(reverse("panel"))
    assert response.status_code == 302
    assert reverse("ingresar") in response.url


@pytest.mark.django_db
def test_votante_recibe_403(client, usuario_votante):
    client.force_login(usuario_votante)
    response = client.get(reverse("panel"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_entra_al_panel(client, usuario_admin):
    client.force_login(usuario_admin)
    response = client.get(reverse("panel"), HTTP_X_INERTIA="true")
    assert response.status_code == 200
    assert response.json()["component"] == "Panel/Inicio"

import json

import pytest
from django.urls import reverse

from cuentas.models import Usuario
from web.json_body import querydict_desde_json


def test_querydict_convierte_booleanos():
    datos = querydict_desde_json(
        {"email": "ana@correo.com", "acepto_tratamiento": True, "otro": False}
    )
    assert datos["email"] == "ana@correo.com"
    assert datos["acepto_tratamiento"] == "True"
    assert datos["otro"] == ""


@pytest.mark.django_db
def test_login_inertia_json_inicia_sesion(client, usuario_admin):
    response = client.post(
        reverse("ingresar"),
        data=json.dumps(
            {"email": usuario_admin.email, "password": "ClaveSegura2027!"}
        ),
        content_type="application/json",
        HTTP_X_INERTIA="true",
    )
    assert response.status_code == 302
    assert response.url == reverse("panel")


@pytest.mark.django_db
def test_login_inertia_json_vacio_marca_obligatorios(client):
    response = client.post(
        reverse("ingresar"),
        data=json.dumps({}),
        content_type="application/json",
        HTTP_X_INERTIA="true",
    )
    assert response.status_code == 200
    errors = response.json()["props"]["errors"]
    assert "email" in errors
    assert "password" in errors


@pytest.mark.django_db
def test_registro_inertia_json(client):
    response = client.post(
        reverse("registro"),
        data=json.dumps(
            {
                "nombre": "Ana Demo",
                "email": "ana.demo@correo.com",
                "password": "ClaveSegura2027!",
                "acepto_tratamiento": True,
            }
        ),
        content_type="application/json",
        HTTP_X_INERTIA="true",
    )
    assert response.status_code == 302
    assert Usuario.objects.filter(email="ana.demo@correo.com").exists()

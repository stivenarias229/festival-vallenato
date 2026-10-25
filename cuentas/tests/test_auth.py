import re

import pytest
from django.core import mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from cuentas.models import Usuario
from cuentas.throttling import limpiar_fallos_login
from cuentas.tokens import token_verificacion


def _props(response):
    return response.json()["props"]


@pytest.mark.django_db
def test_registro_exige_consentimiento(client):
    response = client.post(
        reverse("registro"),
        {
            "nombre": "Ana",
            "email": "ana@correo.com",
            "password": "ClaveSegura2027!",
        },
        HTTP_X_INERTIA="true",
        HTTP_X_INERTIA_VERSION="1",
    )
    assert response.status_code == 200
    assert "acepto_tratamiento" in _props(response)["errors"]
    assert not Usuario.objects.filter(email="ana@correo.com").exists()


@pytest.mark.django_db
def test_registro_y_verificacion(client):
    response = client.post(
        reverse("registro"),
        {
            "nombre": "Ana",
            "email": "ana@correo.com",
            "password": "ClaveSegura2027!",
            "acepto_tratamiento": "on",
        },
    )
    assert response.status_code == 302
    usuario = Usuario.objects.get(email="ana@correo.com")
    assert usuario.acepto_tratamiento
    assert usuario.fecha_tratamiento
    assert not usuario.verificado
    assert mail.outbox
    enlace = re.search(r"/verificar/[^/\s]+/[^/\s]+/", mail.outbox[0].body)
    assert enlace
    client.get(enlace.group(0))
    usuario.refresh_from_db()
    assert usuario.verificado


@pytest.mark.django_db
def test_login_logout_y_bloqueado(client, usuario_votante):
    ok = client.post(
        reverse("ingresar"),
        {"email": usuario_votante.email, "password": "ClaveSegura2027!"},
    )
    assert ok.status_code == 302
    client.get(reverse("salir"))
    usuario_votante.estado = Usuario.Estado.BLOQUEADO
    usuario_votante.save(update_fields=["estado"])
    blocked = client.post(
        reverse("ingresar"),
        {"email": usuario_votante.email, "password": "ClaveSegura2027!"},
        HTTP_X_INERTIA="true",
    )
    assert blocked.status_code == 200
    assert blocked.json()["props"]["errors"]


@pytest.mark.django_db
def test_recuperacion_de_contrasena(client, usuario_votante):
    client.post(reverse("recuperar"), {"email": usuario_votante.email})
    assert mail.outbox
    enlace = re.search(r"/recuperar/[^/\s]+/[^/\s]+/", mail.outbox[0].body)
    assert enlace
    response = client.post(enlace.group(0), {"password": "NuevaClave2027!"})
    assert response.status_code == 302
    usuario_votante.refresh_from_db()
    assert usuario_votante.check_password("NuevaClave2027!")


@pytest.mark.django_db
def test_throttle_de_login(client, usuario_votante, settings):
    settings.LOGIN_MAX_INTENTOS = 2
    limpiar_fallos_login(usuario_votante.email)
    for _ in range(2):
        client.post(
            reverse("ingresar"),
            {"email": usuario_votante.email, "password": "mala"},
            HTTP_X_INERTIA="true",
        )
    response = client.post(
        reverse("ingresar"),
        {"email": usuario_votante.email, "password": "ClaveSegura2027!"},
        HTTP_X_INERTIA="true",
    )
    assert "Demasiados intentos" in str(response.json()["props"]["errors"])


@pytest.mark.django_db
def test_token_verificacion_un_solo_uso(usuario_votante):
    usuario_votante.verificado = False
    usuario_votante.save(update_fields=["verificado"])
    uid = urlsafe_base64_encode(force_bytes(usuario_votante.pk))
    token = token_verificacion.make_token(usuario_votante)
    usuario_votante.verificado = True
    usuario_votante.save(update_fields=["verificado"])
    assert not token_verificacion.check_token(usuario_votante, token)
    assert uid

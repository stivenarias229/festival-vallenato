import pytest
from django.urls import reverse

from auditoria.models import Auditoria
from cuentas.models import Usuario
from votaciones.models import Voto


@pytest.mark.django_db
def test_no_se_bloquea_a_si_mismo(client, usuario_admin):
    client.force_login(usuario_admin)
    response = client.post(
        reverse("panel_usuarios"),
        {"id": usuario_admin.pk, "rol": "votante", "estado": "bloqueado"},
    )
    usuario_admin.refresh_from_db()
    assert usuario_admin.rol == Usuario.Rol.ADMINISTRADOR
    assert usuario_admin.estado == Usuario.Estado.ACTIVO
    assert response.status_code == 302


@pytest.mark.django_db
def test_cambio_de_rol_queda_auditado(client, usuario_admin, usuario_votante):
    client.force_login(usuario_admin)
    client.post(
        reverse("panel_usuarios"),
        {"id": usuario_votante.pk, "rol": "administrador", "estado": "activo"},
    )
    usuario_votante.refresh_from_db()
    assert usuario_votante.rol == Usuario.Rol.ADMINISTRADOR
    assert Auditoria.objects.filter(accion="gestionar_usuario").exists()


@pytest.mark.django_db
def test_props_de_usuarios_sin_password(client, usuario_admin):
    client.force_login(usuario_admin)
    response = client.get(reverse("panel_usuarios"), HTTP_X_INERTIA="true")
    payload = str(response.json()["props"])
    assert "password" not in payload
    assert "contrasena" not in payload


@pytest.mark.django_db
def test_usuario_con_votos_no_se_borra(usuario_votante, catalogo_abierto):
    Voto.objects.create(
        usuario=usuario_votante,
        opcion=catalogo_abierto["opcion"],
        votacion=catalogo_abierto["votacion"],
    )
    from django.db.models.deletion import ProtectedError

    with pytest.raises(ProtectedError):
        usuario_votante.delete()

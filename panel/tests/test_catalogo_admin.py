from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from auditoria.models import Auditoria
from catalogo.models import Votacion


@pytest.mark.django_db
def test_no_abre_votacion_sin_opciones(client, usuario_admin, catalogo_abierto):
    client.force_login(usuario_admin)
    ahora = timezone.now()
    vacia = Votacion.objects.create(
        categoria=catalogo_abierto["categoria"],
        titulo="Sin opciones",
        fecha_inicio=ahora,
        fecha_fin=ahora + timedelta(days=1),
        estado=Votacion.Estado.BORRADOR,
    )
    client.post(reverse("panel_votaciones"), {"accion": "abrir", "id": vacia.pk})
    vacia.refresh_from_db()
    assert vacia.estado == Votacion.Estado.BORRADOR


@pytest.mark.django_db
def test_abrir_votacion_queda_auditado(client, usuario_admin, catalogo_abierto):
    client.force_login(usuario_admin)
    client.post(
        reverse("panel_votaciones"),
        {"accion": "cerrar", "id": catalogo_abierto["votacion"].pk},
    )
    assert Auditoria.objects.filter(accion="cerrar_votacion").exists()

from datetime import timedelta

import pytest
from django.db.models.deletion import ProtectedError
from django.utils import timezone

from catalogo.models import Edicion, Votacion
from votaciones.models import Voto, VotoInmutableError


@pytest.mark.django_db
def test_estado_efectivo_proxima_abierta_cerrada(catalogo_abierto):
    votacion = catalogo_abierto["votacion"]
    ahora = timezone.now()
    votacion.fecha_inicio = ahora + timedelta(days=1)
    votacion.fecha_fin = ahora + timedelta(days=3)
    assert votacion.estado_efectivo(ahora) == "proxima"
    votacion.fecha_inicio = ahora - timedelta(days=1)
    assert votacion.estado_efectivo(ahora) == "abierta"
    votacion.estado = Votacion.Estado.CERRADA
    assert votacion.estado_efectivo(ahora) == "cerrada"


@pytest.mark.django_db
def test_voto_es_inmutable(usuario_votante, catalogo_abierto):
    voto = Voto.objects.create(
        usuario=usuario_votante,
        opcion=catalogo_abierto["opcion"],
        votacion=catalogo_abierto["votacion"],
    )
    voto.opcion = catalogo_abierto["opcion"]
    with pytest.raises(VotoInmutableError):
        voto.save()
    with pytest.raises(VotoInmutableError):
        voto.delete()


@pytest.mark.django_db
def test_usuario_con_votos_no_se_elimina(usuario_votante, catalogo_abierto):
    Voto.objects.create(
        usuario=usuario_votante,
        opcion=catalogo_abierto["opcion"],
        votacion=catalogo_abierto["votacion"],
    )
    with pytest.raises(ProtectedError):
        usuario_votante.delete()


@pytest.mark.django_db
def test_edicion_protect_al_borrar(catalogo_abierto):
    with pytest.raises(ProtectedError):
        catalogo_abierto["edicion"].delete()

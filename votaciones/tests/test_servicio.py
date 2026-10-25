from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import pytest
from django.utils import timezone

from catalogo.models import Opcion, Votacion
from votaciones.models import Voto
from votaciones.services import VotoError, emitir_voto


@pytest.mark.django_db
def test_emite_voto_en_votacion_abierta(usuario_votante, catalogo_abierto):
    voto = emitir_voto(usuario_votante, catalogo_abierto["votacion"], catalogo_abierto["opcion"])
    assert voto.pk
    assert Voto.objects.filter(usuario=usuario_votante).count() == 1


@pytest.mark.django_db
def test_rechaza_votacion_cerrada_o_proxima(usuario_votante, catalogo_abierto):
    votacion = catalogo_abierto["votacion"]
    opcion = catalogo_abierto["opcion"]
    votacion.estado = Votacion.Estado.CERRADA
    votacion.save(update_fields=["estado"])
    with pytest.raises(VotoError):
        emitir_voto(usuario_votante, votacion, opcion)
    votacion.estado = Votacion.Estado.ABIERTA
    votacion.fecha_inicio = timezone.now() + timedelta(days=2)
    votacion.save(update_fields=["estado", "fecha_inicio"])
    with pytest.raises(VotoError):
        emitir_voto(usuario_votante, votacion, opcion)


@pytest.mark.django_db
def test_rechaza_opcion_ajena(usuario_votante, catalogo_abierto):
    otra = Votacion.objects.create(
        categoria=catalogo_abierto["categoria"],
        titulo="Otra",
        fecha_inicio=timezone.now() - timedelta(days=1),
        fecha_fin=timezone.now() + timedelta(days=1),
        estado=Votacion.Estado.ABIERTA,
    )
    opcion_ajena = Opcion.objects.create(votacion=otra, nombre="Ajena", orden=1)
    with pytest.raises(VotoError) as exc:
        emitir_voto(usuario_votante, catalogo_abierto["votacion"], opcion_ajena)
    assert exc.value.codigo == "opcion_ajena"


@pytest.mark.django_db
def test_rechaza_no_verificado_o_bloqueado(catalogo_abierto, db):
    from cuentas.models import Usuario

    pendiente = Usuario.objects.create_user(
        email="pendiente@correo.com",
        password="ClaveSegura2027!",
        nombre="Pendiente",
        verificado=False,
    )
    with pytest.raises(VotoError):
        emitir_voto(pendiente, catalogo_abierto["votacion"], catalogo_abierto["opcion"])
    pendiente.verificado = True
    pendiente.estado = Usuario.Estado.BLOQUEADO
    pendiente.save()
    with pytest.raises(VotoError):
        emitir_voto(pendiente, catalogo_abierto["votacion"], catalogo_abierto["opcion"])


@pytest.mark.django_db
def test_limite_configurable(usuario_votante, catalogo_abierto):
    votacion = catalogo_abierto["votacion"]
    emitir_voto(usuario_votante, votacion, catalogo_abierto["opcion"])
    with pytest.raises(VotoError):
        emitir_voto(usuario_votante, votacion, catalogo_abierto["opcion"])
    votacion.limite_votos_por_usuario = 2
    votacion.save(update_fields=["limite_votos_por_usuario"])
    segundo = emitir_voto(usuario_votante, votacion, catalogo_abierto["opcion"])
    assert segundo.pk


@pytest.mark.django_db(transaction=True)
def test_concurrencia_un_solo_voto(usuario_votante, catalogo_abierto):
    votacion = catalogo_abierto["votacion"]
    opcion = catalogo_abierto["opcion"]

    def intentar():
        try:
            return emitir_voto(usuario_votante, votacion, opcion)
        except VotoError:
            return None

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda _: intentar(), range(2)))
    assert Voto.objects.filter(usuario=usuario_votante, votacion=votacion).count() == 1

from datetime import timedelta

import pytest
from django.utils import timezone

from catalogo.models import Categoria, Edicion, Opcion, Votacion
from cuentas.models import Usuario


@pytest.fixture(autouse=True)
def _entorno_pruebas(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    settings.LOGIN_MAX_INTENTOS = 5
    settings.LOGIN_BLOQUEO_MINUTOS = 15


@pytest.fixture
def usuario_votante(db):
    return Usuario.objects.create_user(
        email="votante@correo.com",
        password="ClaveSegura2027!",
        nombre="Votante Demo",
        verificado=True,
        acepto_tratamiento=True,
        fecha_tratamiento=timezone.now(),
    )


@pytest.fixture
def usuario_admin(db):
    return Usuario.objects.create_superuser(
        email="admin@festival.example",
        password="ClaveSegura2027!",
        nombre="Admin Festival",
    )


@pytest.fixture
def catalogo_abierto(db):
    ahora = timezone.now()
    edicion = Edicion.objects.create(nombre="Edición test", anio=2027, estado=Edicion.Estado.ACTIVA)
    categoria = Categoria.objects.create(
        edicion=edicion,
        nombre="Acordeón",
        descripcion="Categoría de prueba",
        icono="acc",
    )
    votacion = Votacion.objects.create(
        categoria=categoria,
        titulo="Canción favorita",
        fecha_inicio=ahora - timedelta(days=1),
        fecha_fin=ahora + timedelta(days=2),
        estado=Votacion.Estado.ABIERTA,
        reglas="Un voto por persona.",
        visibilidad_resultados=Votacion.Visibilidad.INTERNOS,
        limite_votos_por_usuario=1,
    )
    opcion = Opcion.objects.create(votacion=votacion, nombre="Opción A", descripcion="Artista A", orden=1)
    Opcion.objects.create(votacion=votacion, nombre="Opción B", descripcion="Artista B", orden=2)
    return {
        "edicion": edicion,
        "categoria": categoria,
        "votacion": votacion,
        "opcion": opcion,
    }

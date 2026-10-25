import pytest
from django.core.management import call_command

from catalogo.models import Categoria, Edicion, Votacion
from cuentas.models import Usuario


@pytest.mark.django_db
def test_seed_demo_es_idempotente():
    call_command("seed_demo")
    call_command("seed_demo")
    assert Edicion.objects.filter(nombre__contains="DEMO").count() == 1
    assert Categoria.objects.filter(edicion__nombre__contains="DEMO").count() == 4
    assert Votacion.objects.filter(titulo="Canción favorita del público").count() == 1
    assert Usuario.objects.filter(email="admin@festival.example").count() == 1

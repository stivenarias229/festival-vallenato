import pytest

from auditoria.models import Auditoria, AuditoriaInmutableError
from auditoria.services import registrar_auditoria


@pytest.mark.django_db
def test_auditoria_solo_inserta(usuario_admin):
    registro = registrar_auditoria(usuario_admin, "crear_categoria", "categoria", "Acordeón")
    assert registro.pk
    with pytest.raises(AuditoriaInmutableError):
        registro.detalle = "cambio"
        registro.save()
    with pytest.raises(AuditoriaInmutableError):
        registro.delete()

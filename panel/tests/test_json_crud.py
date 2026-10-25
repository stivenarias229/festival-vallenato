import json

import pytest
from django.urls import reverse

from catalogo.models import Categoria


@pytest.mark.django_db
def test_crear_categoria_via_json_inertia(client, usuario_admin, catalogo_abierto):
    client.force_login(usuario_admin)
    response = client.post(
        reverse("panel_categorias"),
        data=json.dumps(
            {
                "accion": "guardar_categoria",
                "edicion": catalogo_abierto["edicion"].pk,
                "nombre": "Acordeonera DEMO",
                "descripcion": "Mayor y menor",
                "estado": "activa",
                "icono": "acc",
            }
        ),
        content_type="application/json",
        HTTP_X_INERTIA="true",
    )
    assert response.status_code == 302
    assert Categoria.objects.filter(nombre="Acordeonera DEMO").exists()

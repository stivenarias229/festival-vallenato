from catalogo.models import Opcion, Votacion


def reordenar_opcion(votacion: Votacion, opcion: Opcion, direccion: str) -> bool:
    vecinas = list(votacion.opciones.order_by("orden", "id"))
    indice = next(i for i, item in enumerate(vecinas) if item.pk == opcion.pk)
    destino = indice - 1 if direccion == "subir" else indice + 1
    if destino < 0 or destino >= len(vecinas):
        return False
    vecinas[indice], vecinas[destino] = vecinas[destino], vecinas[indice]
    for posicion, item in enumerate(vecinas, start=1):
        item.orden = posicion
    Opcion.objects.bulk_update(vecinas, ["orden"])
    return True

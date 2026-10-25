from django.db import transaction

from catalogo.models import Opcion, Votacion
from cuentas.models import Usuario

from .models import Voto


class VotoError(Exception):
    def __init__(self, mensaje: str, codigo: str = "voto_invalido"):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo


# PENDIENTE DE VALIDACIÓN (P-02, P-08)
def es_elegible(usuario: Usuario, votacion: Votacion) -> bool:
    """Por defecto cualquier usuario verificado y activo puede votar."""
    return usuario.verificado and usuario.esta_activo


def emitir_voto(usuario: Usuario, votacion: Votacion, opcion: Opcion) -> Voto:
    """Registra un voto en una sola transacción (CU-04, RB-01 a RB-04, RB-12)."""
    with transaction.atomic():
        votante = Usuario.objects.select_for_update().get(pk=usuario.pk)

        if not votante.verificado or not votante.esta_activo:
            raise VotoError("Tu cuenta no puede votar ahora.", "cuenta_invalida")

        if votacion.estado_efectivo() != "abierta":
            raise VotoError("Esta votación no está abierta.", "votacion_cerrada")

        if opcion.votacion_id != votacion.pk:
            raise VotoError("La opción no pertenece a esta votación.", "opcion_ajena")

        if not es_elegible(votante, votacion):
            raise VotoError("No eres elegible para esta votación.", "no_elegible")

        # PENDIENTE DE VALIDACIÓN (P-03)
        emitidos = Voto.objects.filter(usuario=votante, votacion=votacion).count()
        if emitidos >= votacion.limite_votos_por_usuario:
            raise VotoError("Ya alcanzaste el límite de votos en esta votación.", "limite")

        return Voto.objects.create(
            usuario=votante,
            opcion=opcion,
            votacion=votacion,
        )

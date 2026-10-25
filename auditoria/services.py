from .models import Auditoria


def registrar_auditoria(usuario, accion: str, entidad: str, detalle: str = "") -> Auditoria:
    return Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        entidad_afectada=entidad,
        detalle=detalle,
    )

from django.conf import settings
from django.db import models


class VotoInmutableError(Exception):
    """Un voto confirmado no se puede modificar ni eliminar (RB-04, RNF-04)."""


class Voto(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="votos",
    )
    opcion = models.ForeignKey(
        "catalogo.Opcion",
        on_delete=models.PROTECT,
        related_name="votos",
    )
    votacion = models.ForeignKey(
        "catalogo.Votacion",
        on_delete=models.PROTECT,
        related_name="votos",
    )
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["votacion"]),
            models.Index(fields=["opcion"]),
            models.Index(fields=["usuario", "votacion"]),
        ]

    def save(self, *args, **kwargs):
        if self.pk and Voto.objects.filter(pk=self.pk).exists():
            raise VotoInmutableError("Un voto confirmado no se puede modificar.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise VotoInmutableError("Un voto confirmado no se puede eliminar.")

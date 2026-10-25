from django.conf import settings
from django.db import models


class AuditoriaInmutableError(Exception):
    """La bitácora solo admite inserciones (RNF-06)."""


class Auditoria(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="auditorias",
    )
    accion = models.CharField(max_length=80)
    entidad_afectada = models.CharField(max_length=80)
    detalle = models.TextField(blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["-fecha_hora"]), models.Index(fields=["accion"])]
        ordering = ["-fecha_hora"]

    def save(self, *args, **kwargs):
        if self.pk and Auditoria.objects.filter(pk=self.pk).exists():
            raise AuditoriaInmutableError("La auditoría no se puede modificar.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise AuditoriaInmutableError("La auditoría no se puede eliminar.")

from django.db import models
from django.utils import timezone


class Edicion(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        INACTIVA = "inactiva", "Inactiva"

    nombre = models.CharField(max_length=150)
    anio = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.INACTIVA)

    class Meta:
        indexes = [models.Index(fields=["estado", "anio"])]
        constraints = [
            models.UniqueConstraint(fields=["nombre", "anio"], name="uniq_edicion_nombre_anio"),
        ]

    def __str__(self) -> str:
        return f"{self.nombre} {self.anio}"


class Categoria(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        INACTIVA = "inactiva", "Inactiva"

    edicion = models.ForeignKey(
        Edicion,
        on_delete=models.PROTECT,
        related_name="categorias",
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVA)
    icono = models.CharField(max_length=30, default="star")

    class Meta:
        indexes = [models.Index(fields=["edicion", "estado"])]

    def __str__(self) -> str:
        return self.nombre


class Votacion(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        ABIERTA = "abierta", "Abierta"
        CERRADA = "cerrada", "Cerrada"

    class Visibilidad(models.TextChoices):
        # PENDIENTE DE VALIDACIÓN (P-04)
        INTERNOS = "internos", "Internos"
        AL_CIERRE = "al_cierre", "Al cierre"
        EN_VIVO = "en_vivo", "En vivo"

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="votaciones",
    )
    titulo = models.CharField(max_length=200)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.BORRADOR)
    reglas = models.TextField(blank=True)
    visibilidad_resultados = models.CharField(
        max_length=20,
        choices=Visibilidad.choices,
        default=Visibilidad.INTERNOS,
    )
    # PENDIENTE DE VALIDACIÓN (P-03)
    limite_votos_por_usuario = models.PositiveSmallIntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(fields=["categoria", "estado"]),
            models.Index(fields=["fecha_inicio", "fecha_fin"]),
        ]

    def __str__(self) -> str:
        return self.titulo

    def estado_efectivo(self, ahora=None) -> str:
        ahora = ahora or timezone.now()
        if self.estado == self.Estado.BORRADOR:
            return "borrador"
        if self.estado == self.Estado.CERRADA:
            return "cerrada"
        if ahora < self.fecha_inicio:
            return "proxima"
        if ahora > self.fecha_fin:
            return "cerrada"
        return "abierta"


class Opcion(models.Model):
    votacion = models.ForeignKey(
        Votacion,
        on_delete=models.PROTECT,
        related_name="opciones",
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="opciones/", blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=["votacion", "orden"])]
        ordering = ["orden", "id"]

    def __str__(self) -> str:
        return self.nombre

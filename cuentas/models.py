from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import ProtectedError


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo es obligatorio.")
        email = self.normalize_email(email)
        extra_fields.setdefault("rol", Usuario.Rol.VOTANTE)
        extra_fields.setdefault("estado", Usuario.Estado.ACTIVO)
        extra_fields.setdefault("nombre", extra_fields.get("nombre", ""))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("verificado", True)
        extra_fields.setdefault("rol", Usuario.Rol.ADMINISTRADOR)
        extra_fields.setdefault("estado", Usuario.Estado.ACTIVO)
        extra_fields.setdefault("nombre", extra_fields.get("nombre", "Administrador"))
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        VOTANTE = "votante", "Votante"
        ADMINISTRADOR = "administrador", "Administrador"

    class Estado(models.TextChoices):
        ACTIVO = "activo", "Activo"
        BLOQUEADO = "bloqueado", "Bloqueado"

    username = None
    email = models.EmailField("correo", unique=True)
    nombre = models.CharField(max_length=150)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.VOTANTE)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVO)
    verificado = models.BooleanField(default=False)
    acepto_tratamiento = models.BooleanField(default=False)
    fecha_tratamiento = models.DateTimeField(null=True, blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]

    class Meta:
        indexes = [
            models.Index(fields=["rol", "estado"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self) -> str:
        return self.nombre or self.email

    @property
    def esta_activo(self) -> bool:
        return self.estado == self.Estado.ACTIVO

    def delete(self, using=None, keep_parents=False):
        if self.votos.exists():
            raise ProtectedError("Un usuario con votos no se elimina.", [self])
        return super().delete(using=using, keep_parents=keep_parents)

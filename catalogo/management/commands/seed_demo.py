from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from catalogo.models import Categoria, Edicion, Opcion, Votacion
from cuentas.models import Usuario

UsuarioModel = get_user_model()

CATEGORIAS_DEMO = [
    ("acc", "Acordeón", "Profesional · aficionado · juvenil · infantil"),
    ("music", "Canción vallenata inédita", "Categoría única"),
    ("mic", "Piquería", "Mayor · infantil"),
    ("star", "Piloneras", "Agrupaciones y comparsas"),
]

VOTACIONES_DEMO = [
    ("Canción favorita del público", "abierta", -2, 7),
    ("Mejor presentación de comparsa", "abierta", -1, 8),
    ("Mejor vestuario de pilonera", "abierta", 3, 10),
    ("Reconocimiento del público", "cerrada", -12, -5),
]

USUARIOS_DEMO = [
    ("Camila Rojas", "camila.rojas@correo.com", Usuario.Rol.VOTANTE, Usuario.Estado.ACTIVO),
    ("Andrés Peña", "andres.pena@correo.com", Usuario.Rol.VOTANTE, Usuario.Estado.ACTIVO),
    ("Laura Mejía", "laura.mejia@correo.com", Usuario.Rol.VOTANTE, Usuario.Estado.BLOQUEADO),
    ("Juan Ortiz", "juan.ortiz@correo.com", Usuario.Rol.VOTANTE, Usuario.Estado.ACTIVO),
    ("Sofía Vargas", "sofia.vargas@correo.com", Usuario.Rol.VOTANTE, Usuario.Estado.ACTIVO),
    ("Admin Festival", "admin@festival.example", Usuario.Rol.ADMINISTRADOR, Usuario.Estado.ACTIVO),
]


class Command(BaseCommand):
    help = "Carga datos DEMO ilustrativos. Idempotente. Pendiente de validación (P-06)."

    def handle(self, *args, **options):
        ahora = timezone.now()
        edicion, _ = Edicion.objects.get_or_create(
            nombre="Festival de la Leyenda Vallenata DEMO",
            anio=2027,
            defaults={"estado": Edicion.Estado.ACTIVA},
        )
        if edicion.estado != Edicion.Estado.ACTIVA:
            edicion.estado = Edicion.Estado.ACTIVA
            edicion.save(update_fields=["estado"])

        categorias = []
        for icono, nombre, descripcion in CATEGORIAS_DEMO:
            categoria, _ = Categoria.objects.get_or_create(
                edicion=edicion,
                nombre=nombre,
                defaults={
                    "descripcion": descripcion,
                    "estado": Categoria.Estado.ACTIVA,
                    "icono": icono,
                },
            )
            categorias.append(categoria)

        acordeon = categorias[0]
        for titulo, estado, inicio_dias, fin_dias in VOTACIONES_DEMO:
            votacion, created = Votacion.objects.get_or_create(
                categoria=acordeon,
                titulo=titulo,
                defaults={
                    "fecha_inicio": ahora + timedelta(days=inicio_dias),
                    "fecha_fin": ahora + timedelta(days=fin_dias),
                    "estado": estado,
                    "reglas": (
                        "Solo puedes votar mientras la votación esté abierta.\n"
                        "Un voto por votación (pendiente de validación, P-03).\n"
                        "Un voto confirmado no se puede cambiar.\n"
                        "Los resultados se publican según la configuración del Festival (P-04)."
                    ),
                    "visibilidad_resultados": Votacion.Visibilidad.INTERNOS,
                    "limite_votos_por_usuario": 1,
                },
            )
            if not created:
                votacion.fecha_inicio = ahora + timedelta(days=inicio_dias)
                votacion.fecha_fin = ahora + timedelta(days=fin_dias)
                votacion.estado = estado
                votacion.save(update_fields=["fecha_inicio", "fecha_fin", "estado"])
            for indice, letra in enumerate(("A", "B", "C"), start=1):
                Opcion.objects.get_or_create(
                    votacion=votacion,
                    nombre=f"Opción {letra}",
                    defaults={
                        "descripcion": f"Artista o agrupación {letra} — DEMO",
                        "orden": indice,
                    },
                )

        for nombre, email, rol, estado in USUARIOS_DEMO:
            usuario, created = UsuarioModel.objects.get_or_create(
                email=email,
                defaults={
                    "nombre": nombre,
                    "rol": rol,
                    "estado": estado,
                    "verificado": True,
                    "acepto_tratamiento": True,
                    "fecha_tratamiento": ahora,
                    "is_staff": rol == Usuario.Rol.ADMINISTRADOR,
                    "is_superuser": email == "admin@festival.example",
                },
            )
            if created:
                usuario.set_password("Festival2027!")
                usuario.save()
            elif email == "admin@festival.example" and not usuario.check_password("Festival2027!"):
                usuario.set_password("Festival2027!")
                usuario.rol = Usuario.Rol.ADMINISTRADOR
                usuario.verificado = True
                usuario.is_staff = True
                usuario.is_superuser = True
                usuario.save()

        self.stdout.write(self.style.SUCCESS("Datos DEMO listos (pendientes de validación)."))

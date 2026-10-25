from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .mail import enviar_correo
from .models import Usuario
from .tokens import token_verificacion


def registrar_votante(nombre: str, email: str, password: str) -> Usuario:
    ahora = timezone.now()
    usuario = Usuario.objects.create_user(
        email=email,
        password=password,
        nombre=nombre,
        rol=Usuario.Rol.VOTANTE,
        estado=Usuario.Estado.ACTIVO,
        verificado=False,
        acepto_tratamiento=True,
        fecha_tratamiento=ahora,
    )
    return usuario


def enviar_correo_verificacion(request, usuario: Usuario) -> None:
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    token = token_verificacion.make_token(usuario)
    enlace = request.build_absolute_uri(reverse("verificar_correo", args=[uid, token]))
    enviar_correo(
        destinatario=usuario.email,
        asunto="Verifica tu cuenta – Festival de la Leyenda Vallenata",
        titulo="Verifica tu cuenta",
        mensaje=(
            f"Hola {usuario.nombre}.\n\n"
            "Confirma tu correo con el botón de un solo uso para activar tu cuenta y poder votar."
        ),
        cta_texto="Confirmar correo",
        cta_url=enlace,
        preheader="Confirma tu correo para votar en el Festival.",
    )


def enviar_correo_recuperacion(request, usuario: Usuario, uid: str, token: str) -> None:
    enlace = request.build_absolute_uri(reverse("restablecer", args=[uid, token]))
    enviar_correo(
        destinatario=usuario.email,
        asunto="Restablece tu contraseña – Festival de la Leyenda Vallenata",
        titulo="Restablece tu contraseña",
        mensaje=(
            f"Hola {usuario.nombre}.\n\n"
            "Usa el botón para crear una nueva contraseña. El enlace es de un solo uso."
        ),
        cta_texto="Restablecer contraseña",
        cta_url=enlace,
        preheader="Crea una nueva contraseña para tu cuenta.",
    )

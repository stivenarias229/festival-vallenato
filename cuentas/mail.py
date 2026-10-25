from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

MARCA = "Festival de la Leyenda Vallenata"
NOTA_PREDETERMINADA = "Si no solicitaste esta acción, puedes ignorar este mensaje."


def renderizar_correo(
    *,
    asunto: str,
    titulo: str,
    mensaje: str,
    cta_texto: str = "",
    cta_url: str = "",
    nota: str = "",
    preheader: str = "",
) -> tuple[str, str]:
    contexto = {
        "marca": MARCA,
        "asunto": asunto,
        "titulo": titulo,
        "mensaje": mensaje,
        "cta_texto": cta_texto,
        "cta_url": cta_url,
        "nota": nota or NOTA_PREDETERMINADA,
        "preheader": preheader or titulo,
    }
    html = render_to_string("correos/layout.html", contexto)
    texto = render_to_string("correos/layout.txt", contexto)
    return html, texto


def enviar_correo(
    *,
    destinatario: str,
    asunto: str,
    titulo: str,
    mensaje: str,
    cta_texto: str = "",
    cta_url: str = "",
    nota: str = "",
    preheader: str = "",
) -> None:
    html, texto = renderizar_correo(
        asunto=asunto,
        titulo=titulo,
        mensaje=mensaje,
        cta_texto=cta_texto,
        cta_url=cta_url,
        nota=nota,
        preheader=preheader,
    )
    correo = EmailMultiAlternatives(
        subject=asunto,
        body=texto,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario],
    )
    correo.attach_alternative(html, "text/html")
    correo.send(fail_silently=False)

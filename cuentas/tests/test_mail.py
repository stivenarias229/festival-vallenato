from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import RequestFactory
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from cuentas.mail import MARCA, renderizar_correo
from cuentas.services import enviar_correo_recuperacion, enviar_correo_verificacion


def test_un_solo_diseno_con_contenido_distinto():
    html_verificacion, texto_verificacion = renderizar_correo(
        asunto="Verifica tu cuenta",
        titulo="Verifica tu cuenta",
        mensaje="Confirma tu correo para votar.",
        cta_texto="Confirmar correo",
        cta_url="https://ejemplo.test/verificar/abc/token/",
    )
    html_recuperacion, texto_recuperacion = renderizar_correo(
        asunto="Restablece tu contraseña",
        titulo="Restablece tu contraseña",
        mensaje="Crea una nueva contraseña.",
        cta_texto="Restablecer contraseña",
        cta_url="https://ejemplo.test/recuperar/abc/token/",
    )

    assert 'data-correo="festival-layout"' in html_verificacion
    assert 'data-correo="festival-layout"' in html_recuperacion
    assert MARCA in html_verificacion
    assert MARCA in html_recuperacion
    assert MARCA in texto_verificacion
    assert "background-color:#e2b75f" in html_verificacion
    assert "Confirmar correo" in html_verificacion
    assert "Restablecer contraseña" in html_recuperacion
    assert "Confirmar correo" not in html_recuperacion
    assert "Restablecer contraseña" not in html_verificacion
    assert "https://ejemplo.test/verificar/abc/token/" in texto_verificacion
    assert "https://ejemplo.test/recuperar/abc/token/" in texto_recuperacion


def test_verificacion_envia_html_y_texto(usuario_votante):
    usuario_votante.verificado = False
    usuario_votante.save(update_fields=["verificado"])
    request = RequestFactory().get("/")
    enviar_correo_verificacion(request, usuario_votante)

    assert len(mail.outbox) == 1
    enviado = mail.outbox[0]
    assert enviado.alternatives
    html, tipo = enviado.alternatives[0]
    assert tipo == "text/html"
    assert 'data-correo="festival-layout"' in html
    assert MARCA in html
    assert "Confirmar correo" in html
    assert "/verificar/" in enviado.body
    assert "/verificar/" in html


def test_recuperacion_reutiliza_el_mismo_diseno(usuario_votante):
    request = RequestFactory().get("/")
    uid = urlsafe_base64_encode(force_bytes(usuario_votante.pk))
    token = default_token_generator.make_token(usuario_votante)
    enviar_correo_recuperacion(request, usuario_votante, uid, token)

    enviado = mail.outbox[0]
    html = enviado.alternatives[0][0]
    assert 'data-correo="festival-layout"' in html
    assert "Restablecer contraseña" in html
    assert reverse("restablecer", args=[uid, token]) in enviado.body
    assert reverse("restablecer", args=[uid, token]) in html

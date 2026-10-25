from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from inertia import render

from auditoria.services import registrar_auditoria

from .forms import IngresoForm, RecuperarForm, RegistroForm, RestablecerForm
from .models import Usuario
from .services import (
    enviar_correo_recuperacion,
    enviar_correo_verificacion,
    registrar_votante,
)
from .throttling import limpiar_fallos_login, registrar_fallo_login
from .tokens import token_verificacion


def registro(request):
    if request.user.is_authenticated:
        return redirect("inicio")
    errors = {}
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = registrar_votante(
                form.cleaned_data["nombre"],
                form.cleaned_data["email"],
                form.cleaned_data["password"],
            )
            enviar_correo_verificacion(request, usuario)
            return redirect("registro_enviado")
        errors = {key: values[0] for key, values in form.errors.items()}
    return render(request, "Auth/Registro", {"errors": errors})


def registro_enviado(request):
    return render(request, "Auth/RegistroEnviado")


def verificar(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(pk=uid)
    except (Usuario.DoesNotExist, ValueError, TypeError, OverflowError):
        usuario = None
    if usuario and token_verificacion.check_token(usuario, token):
        usuario.verificado = True
        usuario.save(update_fields=["verificado"])
        messages.success(request, "Tu correo quedó verificado. Ya puedes ingresar.")
        return redirect("ingresar")
    messages.error(request, "El enlace de verificación no es válido o ya se usó.")
    return redirect("ingresar")


def ingresar(request):
    if request.user.is_authenticated:
        if request.user.rol == Usuario.Rol.ADMINISTRADOR:
            return redirect("panel")
        return redirect(request.GET.get("next") or "categorias")
    errors = {}
    if request.method == "POST":
        form = IngresoForm(request.POST, request=request)
        if form.is_valid():
            usuario = form.usuario
            login(request, usuario)
            limpiar_fallos_login(usuario.email)
            if usuario.rol == Usuario.Rol.ADMINISTRADOR:
                registrar_auditoria(
                    usuario,
                    "inicio_sesion",
                    "usuario",
                    f"Administrador {usuario.email} inició sesión.",
                )
                return redirect(request.POST.get("next") or request.GET.get("next") or "panel")
            if not usuario.verificado:
                messages.info(request, "Debes verificar tu correo antes de votar.")
            return redirect(request.POST.get("next") or request.GET.get("next") or "categorias")
        email = (request.POST.get("email") or "").lower()
        if email:
            registrar_fallo_login(email)
        errors = {key: values[0] for key, values in form.errors.items()}
        if form.non_field_errors() and "password" not in errors:
            errors["password"] = form.non_field_errors()[0]
    return render(
        request,
        "Auth/Ingresar",
        {"errors": errors, "next": request.GET.get("next", "")},
    )


def salir(request):
    logout(request)
    messages.success(request, "Cerraste sesión.")
    return redirect("inicio")


def recuperar(request):
    errors = {}
    if request.method == "POST":
        form = RecuperarForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            usuario = Usuario.objects.filter(email=email).first()
            if usuario:
                uid = urlsafe_base64_encode_safe(usuario.pk)
                token = default_token_generator.make_token(usuario)
                enviar_correo_recuperacion(request, usuario, uid, token)
            messages.success(
                request,
                "Si el correo existe, enviaremos un enlace para restablecer la contraseña.",
            )
            return redirect("ingresar")
        errors = {key: values[0] for key, values in form.errors.items()}
    return render(request, "Auth/Recuperar", {"errors": errors})


def restablecer(request, uidb64, token):
    usuario = _usuario_desde_uid(uidb64)
    if usuario is None or not default_token_generator.check_token(usuario, token):
        messages.error(request, "El enlace de recuperación no es válido o expiró.")
        return redirect("recuperar")
    errors = {}
    if request.method == "POST":
        form = RestablecerForm(request.POST)
        if form.is_valid():
            usuario.set_password(form.cleaned_data["password"])
            usuario.save(update_fields=["password"])
            messages.success(request, "Tu contraseña fue actualizada. Ingresa con la nueva.")
            return redirect("ingresar")
        errors = {key: values[0] for key, values in form.errors.items()}
    return render(request, "Auth/Restablecer", {"errors": errors})


def urlsafe_base64_encode_safe(pk) -> str:
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    return urlsafe_base64_encode(force_bytes(pk))


def _usuario_desde_uid(uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return Usuario.objects.get(pk=uid)
    except (Usuario.DoesNotExist, ValueError, TypeError, OverflowError):
        return None

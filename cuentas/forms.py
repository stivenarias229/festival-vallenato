from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .captcha import captcha_ok
from .models import Usuario
from .throttling import login_bloqueado


class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=150, label="Nombre completo")
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput,
        label="Contraseña",
    )
    acepto_tratamiento = forms.BooleanField(
        label="Autorizo el tratamiento de mis datos personales (Ley 1581 de 2012).",
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def clean_acepto_tratamiento(self):
        if not self.cleaned_data.get("acepto_tratamiento"):
            raise forms.ValidationError("Debes autorizar el tratamiento de tus datos.")
        return True


class IngresoForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        self.usuario = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        email = (cleaned.get("email") or "").lower()
        password = cleaned.get("password")
        if not email or not password:
            return cleaned
        if not captcha_ok(self.request):
            raise forms.ValidationError("No se pudo validar el captcha.")
        if login_bloqueado(email):
            raise forms.ValidationError(
                "Demasiados intentos fallidos. Intenta de nuevo más tarde."
            )
        usuario = authenticate(self.request, username=email, password=password)
        if usuario is None:
            raise forms.ValidationError("Credenciales inválidas.")
        if usuario.estado == Usuario.Estado.BLOQUEADO:
            raise forms.ValidationError("Esta cuenta está bloqueada.")
        self.usuario = usuario
        return cleaned


class RecuperarForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")


class RestablecerForm(forms.Form):
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput,
        label="Nueva contraseña",
    )

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

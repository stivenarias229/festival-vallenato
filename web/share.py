from django.contrib import messages
from django.urls import NoReverseMatch, reverse


def _reverse(name: str, fallback: str) -> str:
    try:
        return reverse(name)
    except NoReverseMatch:
        return fallback


def usuario_compartido(request):
    user = request.user
    if not getattr(user, "is_authenticated", False):
        return None
    return {
        "id": user.pk,
        "nombre": getattr(user, "nombre", "") or user.get_username(),
        "email": getattr(user, "email", ""),
        "rol": getattr(user, "rol", None),
    }


def flash_compartido(request):
    storage = messages.get_messages(request)
    payload = {}
    for message in storage:
        nivel = message.level_tag
        if nivel == "success":
            payload["success"] = str(message)
        elif nivel == "error":
            payload["error"] = str(message)
        else:
            payload["info"] = str(message)
    return payload


def urls_compartidas(_request):
    return {
        "inicio": _reverse("inicio", "/"),
        "registro": _reverse("registro", "/registro"),
        "ingresar": _reverse("ingresar", "/ingresar"),
        "salir": _reverse("salir", "/salir"),
        "categorias": _reverse("categorias", "/categorias"),
        "recuperar": _reverse("recuperar", "/recuperar"),
        "panel": _reverse("panel", "/panel"),
        "panel_categorias": _reverse("panel_categorias", "/panel/categorias"),
        "panel_votaciones": _reverse("panel_votaciones", "/panel/votaciones"),
        "panel_usuarios": _reverse("panel_usuarios", "/panel/usuarios"),
        "panel_resultados": _reverse("panel_resultados", "/panel/resultados"),
        "panel_actividad": _reverse("panel_actividad", "/panel/actividad"),
    }

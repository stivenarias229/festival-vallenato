from django.conf import settings
from django.core.cache import cache

# PENDIENTE DE VALIDACIÓN (RNF-03)


def _clave(identificador: str) -> str:
    return f"login-intentos:{identificador.lower()}"


def login_bloqueado(identificador: str) -> bool:
    data = cache.get(_clave(identificador)) or {"fallos": 0, "bloqueado": False}
    return bool(data.get("bloqueado"))


def registrar_fallo_login(identificador: str) -> None:
    clave = _clave(identificador)
    timeout = settings.LOGIN_BLOQUEO_MINUTOS * 60
    data = cache.get(clave) or {"fallos": 0, "bloqueado": False}
    data["fallos"] = int(data.get("fallos", 0)) + 1
    if data["fallos"] >= settings.LOGIN_MAX_INTENTOS:
        data["bloqueado"] = True
    cache.set(clave, data, timeout)


def limpiar_fallos_login(identificador: str) -> None:
    cache.delete(_clave(identificador))

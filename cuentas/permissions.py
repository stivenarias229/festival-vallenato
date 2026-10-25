from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden

from cuentas.models import Usuario


def requiere_administrador(view):
    """Único control de acceso al panel (P-09). MFA no se implementa."""

    @wraps(view)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url="ingresar")
        if (
            getattr(request.user, "rol", None) != Usuario.Rol.ADMINISTRADOR
            or getattr(request.user, "estado", None) == Usuario.Estado.BLOQUEADO
        ):
            return HttpResponseForbidden("No tienes permiso para entrar al panel.")
        return view(request, *args, **kwargs)

    return _wrapped

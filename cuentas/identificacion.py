# PENDIENTE DE VALIDACIÓN (P-01)
# Identificación del votante aislada para poder cambiar el mecanismo.


def obtener_identificador(usuario) -> str:
    """Devuelve el identificador oficial del votante. Por defecto: correo."""
    return usuario.email

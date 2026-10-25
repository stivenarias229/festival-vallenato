import json

from django.http import QueryDict
from django.utils.datastructures import MultiValueDict


def valor_post(valor) -> str:
    if valor is True:
        return "True"
    if valor is False or valor is None:
        return ""
    return str(valor)


def querydict_desde_json(payload: dict) -> QueryDict:
    post = QueryDict("", mutable=True)
    for clave, valor in payload.items():
        if isinstance(valor, list):
            post.setlist(clave, [valor_post(item) for item in valor])
        else:
            post[clave] = valor_post(valor)
    return post


def cargar_json_en_post(request) -> None:
    """Inertia envía application/json; Django Forms leen request.POST."""
    content_type = request.content_type or ""
    if request.method not in {"POST", "PUT", "PATCH"}:
        return
    if "application/json" not in content_type:
        return
    try:
        crudo = request.body.decode() if request.body else "{}"
        payload = json.loads(crudo or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return
    if not isinstance(payload, dict):
        return
    request._post = querydict_desde_json(payload)
    if not hasattr(request, "_files"):
        request._files = MultiValueDict()

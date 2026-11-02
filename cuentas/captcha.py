import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


def captcha_ok(request) -> bool:
    """Valida el token de Cloudflare Turnstile enviado en el login."""
    secret = getattr(settings, "TURNSTILE_SECRET_KEY", "") or ""
    if not secret:
        logger.warning("TURNSTILE_SECRET_KEY no configurada; captcha rechazado.")
        return False

    token = (request.POST.get("cf-turnstile-response") or "").strip()
    if not token:
        return False

    payload = urllib.parse.urlencode(
        {
            "secret": secret,
            "response": token,
            "remoteip": request.META.get("REMOTE_ADDR", ""),
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        settings.TURNSTILE_VERIFY_URL,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        logger.warning("Fallo al verificar Turnstile: %s", exc)
        return False

    return bool(data.get("success"))

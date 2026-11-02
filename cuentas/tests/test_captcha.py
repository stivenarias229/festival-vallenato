import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory

from cuentas.captcha import captcha_ok


def _request(token: str = "token-ok"):
    factory = RequestFactory()
    request = factory.post("/ingresar", {"cf-turnstile-response": token})
    request.META["REMOTE_ADDR"] = "127.0.0.1"
    return request


@pytest.mark.django_db
def test_captcha_rechaza_sin_token(settings):
    settings.TURNSTILE_SECRET_KEY = "secret"
    request = RequestFactory().post("/ingresar", {})
    assert captcha_ok(request) is False


@pytest.mark.django_db
def test_captcha_rechaza_sin_secret(settings):
    settings.TURNSTILE_SECRET_KEY = ""
    assert captcha_ok(_request()) is False


@pytest.mark.django_db
def test_captcha_ok_con_siteverify_exitoso(settings):
    settings.TURNSTILE_SECRET_KEY = "secret"
    settings.TURNSTILE_VERIFY_URL = "https://example.test/siteverify"
    body = json.dumps({"success": True}).encode("utf-8")
    mock_resp = MagicMock()
    mock_resp.read.return_value = body
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = False

    with patch("urllib.request.urlopen", return_value=mock_resp) as urlopen:
        assert captcha_ok(_request("token-ok")) is True
        urlopen.assert_called_once()


@pytest.mark.django_db
def test_captcha_falla_si_siteverify_niega(settings):
    settings.TURNSTILE_SECRET_KEY = "secret"
    body = json.dumps({"success": False, "error-codes": ["invalid-input-response"]}).encode(
        "utf-8"
    )
    mock_resp = MagicMock()
    mock_resp.read.return_value = body
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.__exit__.return_value = False

    with patch("urllib.request.urlopen", return_value=mock_resp):
        assert captcha_ok(_request("malo")) is False


@pytest.mark.django_db
def test_captcha_falla_ante_error_de_red(settings):
    settings.TURNSTILE_SECRET_KEY = "secret"
    with patch("urllib.request.urlopen", side_effect=TimeoutError("timeout")):
        assert captcha_ok(_request()) is False

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent


def env_str(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip().strip("'\"")


def env_bool(name: str, default: str = "False") -> bool:
    return env_str(name, default).lower() in {"1", "true", "yes"}


def env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in env_str(name, default).split(",") if item.strip()]


SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "clave-solo-para-desarrollo-cambiar-en-env",
)
DEBUG = env_bool("DEBUG", "True")
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")
if DEBUG:
    for host in ("localhost", "127.0.0.1", "testserver"):
        if host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(host)
CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:8000,http://127.0.0.1:8000",
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_vite",
    "inertia",
    "web",
    "cuentas",
    "catalogo",
    "votaciones",
    "resultados",
    "auditoria",
    "panel",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "web.middleware.InertiaJsonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "web.middleware.InertiaShareMiddleware",
    "inertia.middleware.InertiaMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "aplicacion"),
        "USER": os.environ.get("DB_USER", "root"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

AUTH_USER_MODEL = "cuentas.Usuario"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
_frontend_dist = BASE_DIR / "frontend" / "dist"
STATICFILES_DIRS = [_frontend_dist] if _frontend_dist.is_dir() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "festival-votaciones",
    }
}

LOGIN_URL = "ingresar"
LOGIN_REDIRECT_URL = "inicio"
LOGOUT_REDIRECT_URL = "inicio"

# PENDIENTE DE VALIDACIÓN (RNF-03)
LOGIN_MAX_INTENTOS = int(os.environ.get("LOGIN_MAX_INTENTOS", "5"))
LOGIN_BLOQUEO_MINUTOS = int(os.environ.get("LOGIN_BLOQUEO_MINUTOS", "15"))

EMAIL_BACKEND = env_str(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = env_str("EMAIL_HOST", "sandbox.smtp.mailtrap.io")
EMAIL_PORT = int(env_str("EMAIL_PORT", "2525") or "2525")
EMAIL_HOST_USER = env_str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env_str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", "True")
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", "False")
DEFAULT_FROM_EMAIL = env_str(
    "DEFAULT_FROM_EMAIL",
    "Festival Vallenato <no-reply@festival.local>",
)

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", "False")
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", "False")
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", "False")
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if not DEBUG else None

DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "dev_server_host": "localhost",
        "dev_server_port": 5173,
        "manifest_path": BASE_DIR / "frontend" / "dist" / "manifest.json",
    }
}

INERTIA_LAYOUT = "base.html"

"""
Configuración principal del proyecto Ecotech (Django) 

Este módulo contiene todas las configuraciones globales del proyecto:
apps instaladas, middleware, plantillas, archivos estáticos,
seguridad (DEBUG) e internacionalización.


Estructura de rutas (importante):
- La raíz del proyecto (donde está manage.py) es:
  C:\\Users\\Daniel Vera\\Desktop\\ecotech\\ecotech\\
- El paquete de configuración es `ecotech/` (esta carpeta).
- La app de negocio es `sustentabilidad/`.

"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Rutas base
# ---------------------------------------------------------------------------

# BASE_DIR apunta a la carpeta que contiene manage.py.
# Sin base de datos, solo se usa para rutas de estáticos/templates.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Configuración de seguridad y depuración
# ---------------------------------------------------------------------------

# SECURITY WARNING: cambiar en producción.
SECRET_KEY = "django-insecure-ecotech-dev-key-cambiar-en-produccion"

# DEBUG=True muestra trazas de error detalladas. Solo para desarrollo.
DEBUG = True

# Hosts permitidos. Vacío + DEBUG=True permite localhost.
ALLOWED_HOSTS = []

# ---------------------------------------------------------------------------
# Aplicaciones instaladas 
# ---------------------------------------------------------------------------
# 'sustentabilidad' es la app propia del proyecto y DEBE estar aquí.
# Sin esta línea, Django no carga los templates ni las URLs de la app
# y se produce error 404 / TemplateDoesNotExist.
#
# NO se incluyen admin/auth/sessions/messages porque usan la DB.
# Si algún día se quiere persistir consumos, se agregan y se activa SQLite.

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "sustentabilidad",
]

# ---------------------------------------------------------------------------
# Middleware (procesamiento de la petición/respuesta)
# Sin Session/Auth/Message: esos exigen base de datos / usuarios.
# ---------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------------------------
# URLs y plantillas
# ---------------------------------------------------------------------------

# ROOT_URLCONF: módulo donde Django busca las URLs principales.
# Equivale a `ecotech/ecotech/urls.py`.
ROOT_URLCONF = "ecotech.urls"

# Configuración de plantillas HTML.
# APP_DIRS=True permite que Django busque en `templates/` de cada app,
# por ejemplo: `sustentabilidad/templates/sustentabilidad/panel.html`.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            # Solo 'request': los context_processors de auth/messages
            # necesitan las apps auth/messages (con DB).
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "ecotech.wsgi.application"



# Sin DB: diccionario vacío a propósito. No hay conexión ninguna.
DATABASES = {}

# ---------------------------------------------------------------------------
# Validadores de contraseña: deshabilitados sin auth.
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = []

# ---------------------------------------------------------------------------
# Internacionalización
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Archivos estáticos (CSS, JS, imágenes)
# ---------------------------------------------------------------------------

STATIC_URL = "static/"

# ---------------------------------------------------------------------------
# Email (motor de consola para desarrollo, no envía correos reales)
# ---------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

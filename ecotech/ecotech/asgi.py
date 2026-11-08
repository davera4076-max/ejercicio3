"""
Punto de entrada ASGI para despliegues asíncronos (ej: Daphne, Uvicorn).

Equivalente asíncrono de `wsgi.py`. En desarrollo con `runserver`
no se usa, pero se deja creado para que el proyecto esté completo.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecotech.settings")

application = get_asgi_application()

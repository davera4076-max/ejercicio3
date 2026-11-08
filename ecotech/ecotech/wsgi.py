"""
Punto de entrada WSGI para despliegues (ej: Gunicorn, mod_wsgi).

Django expone `application` para que el servidor web pueda
importar y ejecutar el proyecto. En desarrollo se usa
`python manage.py runserver`, que usa su propio servidor WSGI.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecotech.settings")

application = get_wsgi_application()

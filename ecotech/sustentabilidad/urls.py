"""
URLs de la app `sustentabilidad`.

En Django, cada app puede tener su propio `urls.py` con rutas relativas.
Este archivo se incluye desde `ecotech/urls.py` con `include()`.

Rutas definidas (relativas):
- "" (vacío) -> `vista_panel_sustentabilidad`
  Esto significa:
    - Como se incluye en "" (raíz) => GET / apunta al panel.
    - Como se incluye en "panel/" => GET /panel/ apunta al panel.

Nombre de ruta (name):
- "panel_sustentabilidad": permite usar `{% url 'panel_sustentabilidad' %}`
  en templates y `reverse()` en código.

Para agregar una ruta nueva, agregar una línea `path()` por cada evento.
"""

from django.urls import path

from . import views

urlpatterns = [
    # Evento: panel principal (GET / y GET /panel/).
    path("", views.vista_panel_sustentabilidad, name="panel_sustentabilidad"),
]

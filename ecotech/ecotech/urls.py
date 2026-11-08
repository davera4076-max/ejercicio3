"""
Configuración de URLs del proyecto Ecotech (sin DB / sin admin).

Este archivo es el punto de entrada de todo el enrutamiento.
Como el proyecto es SIN base de datos, no hay `admin/`:
- `panel/` y `/` -> vistas de la app `sustentabilidad`
  (se incluye el `urls.py` de la app).

Ejemplos:
    http://127.0.0.1:8000/panel/  -> panel de sustentabilidad
    http://127.0.0.1:8000/        -> panel de sustentabilidad (raíz)
    http://127.0.0.1:8000/admin/  -> 404 (no hay admin sin DB)
"""

from django.urls import include, path

urlpatterns = [
    # Raíz del sitio: delega en la app sustentabilidad.
    path("", include("sustentabilidad.urls")),
    # Ruta explícita /panel/ : también delega en la app.
    # Se mantiene por compatibilidad con lo que el usuario espera en el navegador.
    path("panel/", include("sustentabilidad.urls")),
]

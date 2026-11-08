"""
Administración de Django para `sustentabilidad`.

En Django, el panel `/admin/` permite ver/editar modelos
si se registran aquí con `admin.register`. Como la app
actualmente no tiene modelos, no se registra nada.

Para registrar un modelo futuro, usar:
    from .models import RegistroConsumo
    admin.site.register(RegistroConsumo)
"""

from django.contrib import admin

# Sin modelos para registrar por ahora.

"""
Modelos de datos de la app `sustentabilidad`.

En Django, un *modelo* es una clase Python que mapea a una tabla
de base de datos. Por ahora la app no usa base de datos: los
registros de consumo se manejan como listas de dicts en `views.py`
y `service.py` (datos de ejemplo).

Si a futuro se quiere persistir consumos, aquí se definiría algo como:

    class RegistroConsumo(models.Model):
        planta = models.CharField(max_length=100)
        consumo_kwh = models.FloatField()
        fecha = models.DateTimeField(auto_now_add=True)

    Y se generaría la migración con `python manage.py makemigrations`.
"""

from django.db import models

# Por ahora no hay modelos. Se deja el import de `models`
# para que el archivo sea válido y listo para extender.

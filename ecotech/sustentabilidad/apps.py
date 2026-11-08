"""
Configuración de la app `sustentabilidad`.

En Django, cada app tiene una clase de configuración (AppConfig)
que define su nombre y comportamiento. Django la descubre
automáticamente al estar `sustentabilidad` en INSTALLED_APPS.
"""

from django.apps import AppConfig


class SustentabilidadConfig(AppConfig):
    """
    Configuración de la app sustentabilidad.

    Atributos:
        default_auto_field: tipo de clave primaria por defecto
            para modelos futuros (BigAutoField, recomendado).
        name: nombre del paquete Python de la app. Debe coincidir
            con la carpeta `sustentabilidad/` (minúsculas, sin espacios).
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "sustentabilidad"

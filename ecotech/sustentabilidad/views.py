# sustentabilidad/views.py
"""
Vistas (eventos HTTP) de la app `sustentabilidad`.

En Django, una *vista* es una función que recibe un request HTTP
(`HttpRequest`) y devuelve una respuesta (`HttpResponse` o render
de template). Este módulo define las vistas públicas de la app.

Contenido:
- `vista_panel_sustentabilidad()`: GET / y GET /panel/
  Muestra el panel con total de emisiones, planta con mayor
  consumo y detalle por planta.

Flujo:
    1. Se definen los registros históricos (datos de ejemplo).
    2. Se calculan métricas con `service.obtener_metricas_consumo()`.
    3. Se arma el contexto (variables para el template).
    4. Se renderiza `sustentabilidad/panel.html`.
"""

from django.shortcuts import render

from .service import obtener_metricas_consumo


def vista_panel_sustentabilidad(request):
    """
    Evento: vista del panel de sustentabilidad.

    URL:
        GET /         -> path("", ...) en sustentabilidad/urls.py
        GET /panel/   -> path("", ...) incluido bajo "panel/" en ecotech/urls.py

    Método:
        GET (lectura). No crea ni modifica datos, solo muestra el panel.
        Si se quiere POST (ej: formulario para agregar consumos),
        habría que extender esta vista y agregar el manejo de request.POST.

    Datos de entrada:
        - `request` (HttpRequest): objeto Django con método, usuario,
          cabeceras, etc. En esta vista no se usa ningún parámetro GET/POST;
          los registros son fijos de ejemplo.

    Lógica (pasos):
        1. Construye `registros_historicos` (lista de dicts planta/consumo).
        2. Llama `obtener_metricas_consumo()` para calcular totales.
        3. Construye `contexto` con las variables exactas que el
           template `panel.html` espera:
              - "total_global_emisiones" (float)
              - "emisiones_por_planta" (dict)
              - "planta_mayor_consumo" (str|None)
        4. Renderiza el template.

    Template usado:
        "sustentabilidad/panel.html"
        Archivo físico: sustentabilidad/templates/sustentabilidad/panel.html
        (Django lo encuentra porque APP_DIRS=True en settings.py).

    Retorna:
        HttpResponse con el HTML del panel.
        Si el template no existe o el cálculo falla (ej: consumo negativo),
        Django mostrará TemplateDoesNotExist / 500 según DEBUG.

    Ejemplo de respuesta (valores):
        Total: 6180.2 kg CO2
        Planta mayor: Planta Tupungato (3120.2 kg CO2)
    """
    # Datos históricos de ejemplo (en un proyecto real vendrían
    # de una base de datos o de una API).
    registros_historicos = [
        {"planta": "Planta Tupungato", "consumo_kwh": 3000.50},
        {"planta": "Planta Tupungato", "consumo_kwh": 4800},
        {"planta": "Planta Tunuyán", "consumo_kwh": 2000},
        {"planta": "Planta San Carlos", "consumo_kwh": 1500},
        {"planta": "Planta San Rafael", "consumo_kwh": 2050},
        {"planta": " ", "consumo_kwh": 2100},
    ]

    # Cálculo de métricas (ver service.py para la documentación completa).
    metricas = obtener_metricas_consumo(registros_historicos)

    # Variables que el template usa: {{ total_global_emisiones }},
    # {{ planta_mayor_consumo }} y {{ emisiones_por_planta.items }}.
    # Los nombres deben coincidir EXACTAMENTE con panel.html.
    contexto = {
        "total_global_emisiones": metricas["total_global_emisiones"],
        "emisiones_por_planta": metricas["emisiones_por_planta"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
    }

    return render(request, "sustentabilidad/panel.html", contexto)
